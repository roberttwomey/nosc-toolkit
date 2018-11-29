/**
  Data streaming from the Shadow motion capture system into the Unity game
  engine. Implemented as a Unity MonoBehaviour controller class.

  @file    tools/plugin/unity/ShadowBehaviour.cs
  @author  Luke Tokheim, luke@motionshadow.com
  @version 2.2

  Copyright (c) 2015, Motion Workshop
*/
using UnityEngine;
using Motion.SDK;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Xml;

namespace Motion {

/**
  Utility class to store information about a Shadow joint node. Convert from
  the Shadow axis convention into the Unity axis convention.
 */
public class ShadowNode {
  /**
   @param  transform UnityEngine.Transform associated with a Shadow skeleton
           node
   */
  public ShadowNode(Transform transform) {
    if (transform) {
      m_transform = transform;
    } else {
      m_transform = new GameObject().transform;
    }

    m_rest = m_transform.localRotation;
    m_update_position = (0 == m_transform.name.IndexOf("Hips"));
  }

  /**
    @param  data 8 element array, quaternion followed by a weighted position,
            [qw, qx, qy, qz, cw, cx, cy, cz].
   */
  public void update(float[] data) {
    // Current local quaternion. Shadow is specified in [w, x, y, z] order but
    // Unity uses [x, y, z, w] order. Also, reflect about the YZ plane since
    // Shadow is right handed and Unity is left handed.
    Quaternion Lq = new Quaternion(-data[1], data[2], data[3], -data[0]);

    m_transform.localRotation = m_rest * Lq;

    if (m_update_position) {
      m_transform.position = new Vector3(-data[5], data[6], data[7]) * 0.01f;
    }
  }

  private Transform m_transform;
  private Quaternion m_rest;
  private bool m_update_position;
} // class ShadowNode

/**
  Unity controller class. Attach to a hierarchy of transforms. Use name matching
  to connect the streaming Shadow nodes to the transform objects in the Unity
  scene. Use the Motion.SDK classes to stream data in a coroutine.
 */
public class ShadowBehaviour : MonoBehaviour {

  // Name or address of the Motion Service.
  public string host = "127.0.0.1";

  // Use this for initialization
  void Start() {
    m_stream.Start(host);
  }

  // Update is called once per frame
  void Update() {
    lock (m_stream) {
      // Print any messages from the stream thread.
      if (m_stream.message.Length > 0) {
        if (Debug.isDebugBuild) {
          Debug.Log(m_stream.message);
        }
        m_stream.message = "";
      }

      if (null == m_stream.data) {
        return;
      }

      // Check from an XML channel definition. This arrives in the data stream
      // whenever it changes.
      if ((0 == m_node_map.Count) && (m_stream.xml.Length > 0)) {
        if (ParseXML(m_stream.xml)) {
          if (Debug.isDebugBuild) {
            Debug.Log(
              "Parsed channel list from data stream, found " +
              m_node_map.Count + " nodes");
          }
        } else if (Debug.isDebugBuild) {
          Debug.LogWarning(
            "Data stream channel list does not match any objects in Unity scene");
        }
        
        m_stream.xml = "";
      }

      // Update Unity transforms based on the most recent sample.
      IDictionary<int, Format.ConfigurableElement> container =
        Format.Configurable(m_stream.data);
      foreach (KeyValuePair<int, Format.ConfigurableElement> itr in container) {
        if (m_node_map.ContainsKey(itr.Key)) {
          ShadowNode node = m_node_map[itr.Key];
          node.update(itr.Value.getRange(0, 8));
        }
      }
    }
  }

  void OnDestroy() {
    m_stream.Stop();
  }

  /**
    Create a mapping from the Motion Service data stream to the current Unity
    scene.

    @param  xml XML formatted string from the Motion Service that specifies the
            names of the nodes in the data stream
    @post   We have a mapping from integer key to objects in the Unity scene
            matched by name.
   */
  private bool ParseXML(string xml) {
    bool result = false;

    // Listing of channel int keys and string names.
    // <node key="1" id="Hips"> ...
    XmlDocument doc = new XmlDocument();
    doc.LoadXml(xml);

    foreach (XmlNode item in doc.DocumentElement.GetElementsByTagName("node")) {
      // Search this subtree for a named node.
      Transform node = FindNode(transform, item.Attributes["id"].Value);
      if (null != node) {
        m_node_map.Add(
          Convert.ToInt32(item.Attributes["key"].Value),
          new ShadowNode(node));
        result = true;
      }      
    }

    return result;
  }

  /**
    Search a tree of Unity transforms for a named object. Return the first one
    that matches by name.

    @param  node UnityEngine.Transform that defines the hierarchy to search in
    @param  name match nodes by string name equality
    @return The first UnityEngine.Transform in the node tree that matches the
            name parameter.
   */
  private Transform FindNode(Transform node, string name) {
    if (name == node.name) {
      return node;
    }

    foreach (Transform child in node.transform) {
      Transform tmp = FindNode(child, name);
      if (null != tmp) {
        return tmp;
      }
    }

    return null;
  }

  private ShadowStream m_stream = new ShadowStream();
  private Dictionary<int, ShadowNode> m_node_map =
    new Dictionary<int, ShadowNode>();
} // class ShadowBehaviour

} // namespace Motion
