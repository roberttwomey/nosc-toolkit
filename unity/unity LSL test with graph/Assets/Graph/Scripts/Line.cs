using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Line {
  internal List<float> dataset;
  internal List<float> LiveValue;
  internal List<GameObject> gameObjectList;
  internal Color color;
  internal int pointLimit = 20;

  public Line (Color c, float initial){
    color = c;
    dataset = new List<float>(new float[22]);
    LiveValue = dataset.GetRange(dataset.Count - pointLimit - 1, pointLimit);
    gameObjectList = new List<GameObject>(){};
  }

  public void runLive(float newVal){
    dataset.Add(newVal);
    LiveValue = dataset.GetRange(dataset.Count - pointLimit - 1, pointLimit);
  }

}
