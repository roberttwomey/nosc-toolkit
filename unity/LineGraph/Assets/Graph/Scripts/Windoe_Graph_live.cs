using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Windoe_Graph_live : MonoBehaviour
{
    
    // Graph Setup
    public int number_of_channels = 3;
    private Graph graph;
    private List<float> sample = new List<float>();

    // Graph Setup
    public float yMaximum;
    public int pointLimit;


    [SerializeField] private Sprite circleSprite;
    private RectTransform graphContainer;
    private RectTransform labelTemplateX;
    private RectTransform labelTemplateY;
    private RectTransform dashTemplateX;
    private RectTransform dashTemplateY;

    void Start()
    {
    }

    private void Awake()
    {
        graphContainer = transform.Find("graphContainer").GetComponent<RectTransform>();
        labelTemplateX = graphContainer.Find("labelTemplateX").GetComponent<RectTransform>();
        labelTemplateY = graphContainer.Find("labelTemplateY").GetComponent<RectTransform>();
        dashTemplateX = graphContainer.Find("dashTemplateY").GetComponent<RectTransform>();
        dashTemplateY = graphContainer.Find("dashTemplateX").GetComponent<RectTransform>();

        // Default Graph
        graph = new Graph(number_of_channels, pointLimit, yMaximum);

        ShowGraph(graph);

    }

    private void Update()
    {
        float newVal1 = UnityEngine.Random.Range(0f, 1.0f);
        float newVal2 = UnityEngine.Random.Range(0f, 1.0f);
        float newVal3 = UnityEngine.Random.Range(0f, 1.0f);

        float[] sample = new float[] { newVal1, newVal2, newVal3 };

        //setting up parallel line graph accoding to input channels
        for (int i = 0; i < number_of_channels; i++)
        {
            graph.lines[i].runLive(sample[i]);
        }


        ShowGraph(graph);
    }

    private GameObject CreateCircle(Vector2 anchoredPosition)
    {
        GameObject gameObject = new GameObject("circle", typeof(Image));
        gameObject.transform.SetParent(graphContainer, false);
        gameObject.GetComponent<Image>().sprite = circleSprite;
        RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
        rectTransform.anchoredPosition = anchoredPosition;
        rectTransform.sizeDelta = new Vector2(2, 2);
        rectTransform.anchorMin = new Vector2(0, 0);
        rectTransform.anchorMax = new Vector2(0, 0);
        return gameObject;
    }

    public void ShowGraph(Graph graph)
    {
        for (int i = 0; i < number_of_channels; i++)
        {
            DrawLine(graph.lines[i], i);
        }
    }

    public void DrawLine(Line line, int line_pos, Func<int, String> getAxisLabelX = null, Func<float, String> getAxisLabelY = null)
    {

        // Test for label defaults
        if (getAxisLabelX == null)
        {
            getAxisLabelX = delegate (int _i) { return _i.ToString(); };
        }
        if (getAxisLabelY == null)
        {
            getAxisLabelY = delegate (float _f) { return _f.ToString(); };
        }

        if (line.gameObjectList.Count != 0)
        {
            // Clean up previous graph
            foreach (GameObject gameObject in line.gameObjectList)
            {
                Destroy(gameObject);
            }
            line.gameObjectList.Clear();
        }

        float graphHeight = graphContainer.sizeDelta.y;
        float graphWidth = graphContainer.sizeDelta.x;
        float xSize = graphWidth / pointLimit;
        float ySize = graphHeight / number_of_channels;

        GameObject lastCircleGameObject = null;
        for (int i = 0; i < line.dataset.Count; i++)
        {
            float xPosition = i * xSize;
            float yPosition = line_pos * ySize + (line.dataset[i] / yMaximum) * ySize;
            GameObject circleGameObject = CreateCircle(new Vector2(xPosition, yPosition));
            line.gameObjectList.Add(circleGameObject);

            if (lastCircleGameObject != null)
            {
                GameObject dotConnectionGameObject = CreateDotConnection(line, lastCircleGameObject.GetComponent<RectTransform>().anchoredPosition, circleGameObject.GetComponent<RectTransform>().anchoredPosition);
                line.gameObjectList.Add(dotConnectionGameObject);
            }
            lastCircleGameObject = circleGameObject;
            
            // Duplicate the x dash template
            RectTransform dashX = Instantiate(dashTemplateX);
            dashX.SetParent(graphContainer, false);
            dashX.gameObject.SetActive(true);
            dashX.anchoredPosition = new Vector2(xPosition, 0);
            line.gameObjectList.Add(dashX.gameObject);
        }

        for (int i = 0; i <= number_of_channels; i++)
        {
            RectTransform labelY = Instantiate(labelTemplateY);
            labelY.SetParent(graphContainer, false);
            labelY.gameObject.SetActive(true);
            float normalizedVal = i * 1f / number_of_channels;
            labelY.anchoredPosition = new Vector2(-20f, normalizedVal * graphHeight - 10f);
            labelY.GetComponent<Text>().text = getAxisLabelY(i);
            line.gameObjectList.Add(labelY.gameObject);

            // Duplicate the dash template
            RectTransform dashY = Instantiate(dashTemplateY);
            dashY.SetParent(graphContainer, false);
            dashY.gameObject.SetActive(true);
            dashY.anchoredPosition = new Vector2(0, normalizedVal * graphHeight);
            line.gameObjectList.Add(dashY.gameObject);
        }
    }

    private GameObject CreateDotConnection(Line line, Vector2 dotPositionA, Vector2 dotPositionB)
    {
        GameObject gameObject = new GameObject("dotConnection", typeof(Image));
        gameObject.transform.SetParent(graphContainer, false);
        gameObject.GetComponent<Image>().color = line.color;
        RectTransform rectTransform = gameObject.GetComponent<RectTransform>();
        Vector2 dir = (dotPositionB - dotPositionA).normalized;
        float distance = Vector2.Distance(dotPositionA, dotPositionB);
        rectTransform.anchorMin = new Vector2(0, 0);
        rectTransform.anchorMax = new Vector2(0, 0);
        rectTransform.sizeDelta = new Vector2(distance, 1f);
        rectTransform.anchoredPosition = dotPositionA + dir * distance * .5f;
        rectTransform.localEulerAngles = new Vector3(0, 0, GetAngleFromVectorFloat(dir));
        return gameObject;
    }

    public static float GetAngleFromVectorFloat(Vector3 dir)
    {
        dir = dir.normalized;
        float n = Mathf.Atan2(dir.y, dir.x) * Mathf.Rad2Deg;
        if (n < 0) n += 360;

        return n;
    }
}
