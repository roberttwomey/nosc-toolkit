using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using UnityEngine.UI;

public class Line {
  internal List<float> dataset;
  internal List<float> LiveValue;
  internal List<GameObject> gameObjectList;
  internal Color color;
  internal int pointLimit;

  public Line (Color c, float initial, int point_Limit){
    color = c;
    pointLimit = point_Limit;
    dataset = new List<float>();
    dataset.AddRange(Enumerable.Repeat(initial, point_Limit+1));
    LiveValue = dataset.GetRange(dataset.Count - pointLimit - 1, pointLimit);
    gameObjectList = new List<GameObject>(){};
  }

  public void runLive(float newVal){
    dataset.Add(newVal);
    LiveValue = dataset.GetRange(dataset.Count - pointLimit - 1, pointLimit);
  }

}
