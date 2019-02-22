/**
  Data streaming from the Shadow motion capture system into the Unity game
  engine. This class manages a thread that streams data from the Motion Service
  at a frame rate independent of Unity.

  @file    tools/plugin/unity/ShadowStream.cs
  @author  Luke Tokheim, luke@motionshadow.com
  @version 2.2

  Copyright (c) 2015, Motion Workshop
*/
using Motion.SDK;
using System;
using System.Threading;
using UnityEngine;

namespace Motion {

/**
  Container class for all data shared from our Motion SDK stream thread back to
  the Unity UI thread.
*/
public class ShadowStream {
  public byte[] data = null;
  public string xml = "";
  public string message = "";

        /**
         Safe to call from the Unity UI thread. Start sampling data and load it into
         the public members of this instance. The UI thread can safely access the
         data using the "lock (this)" semantics.
        */
        public void Start(string host)
        {
            m_thread = new Thread(ThreadLoop);
            m_thread.Start(host);
        }

  /**
    Safe to call from the Unity UI thread. Stop the sampling thread.
   */
  public void Stop() {
    lock (this) {
      m_quit = true;
    }

    if (!m_thread.Join(1000)) {
      m_thread.Abort();
    }
  }

  /**
    Internal thread loop function. Read samples as quickly as possible and load
    the most recent one into our public member state.
   */ 
  private void ThreadLoop(object host) {
    while (true) {
      // Initialize the data stream connection to the Motion Service.
      Client client = new Client(host.ToString(), 32076);
      if (!client.isConnected()) {
        lock (this) {
          message =
            "Failed to connect to Motion Service at " + host;
        }

        continue;
      }

      // Request local quaternion and constraint position channels. Also, get
      // the "inactive" channels which includes interpolated nodes in a
      // hierarchy and the end effectors.
      client.writeData(
        "<?xml version=\"1.0\"?>" +
        "<configurable inactive=\"1\">" +
        "<Lq/><c/>" +
        "</configurable>");

      lock (this) {
        message = "Connected to Motion Service at " + host;
      }

      bool reading = false;
      while (client.isConnected()) {
        byte[] _data = client.readData();

        // We may need to refresh our XML channel definition when there is
        // an interruption in the data stream.
        string _xml = null;
        if (null != _data) {
          if (!reading) {
            _xml = client.getXMLString();
            if (_xml.Length > 0) {
              reading = true;
            }
          }
        } else if (reading) {
          reading = false;
          lock (this) {
            message =
              "Data stream interrupted, waiting for next sample";
          }
        }

        // Copy temporary locals into the protected state variables.
        lock (this) {
          data = _data;
          if (null != _xml) {
            xml = _xml;
          }

          if (m_quit) {
            break;
          }
        }
      }

      client.close();
      client = null;

      lock (this) {
        data = null;
        xml = "";
        message = "Disconnected from Motion service";

        if (m_quit) {
          break;
        }
      }
    }
  }

  private Thread m_thread = null;
  private bool m_quit = false;
} // class ShadowStream

} // namespace Motion
