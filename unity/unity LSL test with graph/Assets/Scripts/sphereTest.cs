﻿using System.Collections;
using UnityEngine;
using Assets.LSL4Unity.Scripts;
using Assets.LSL4Unity.Scripts.AbstractInlets;

public class sphereTest : InletFloatSamples
{
    public Vector3 sphereSize = new Vector3 (1, 1, 1);
    public Color sphereColor = new Color(100, 100, 100);

    public bool useX;
    public bool useY;
    public bool useZ;

    private bool pullSamplesContinuously = false;
    private int interval = 0;


    void Start()
    {
        // [optional] call this only, if your gameobject hosting this component
        // got instantiated during runtime
        Debug.Log("start sphere");

        registerAndLookUpStream();
    }

    protected override bool isTheExpected(LSLStreamInfoWrapper stream)
    {
        // the base implementation just checks for stream name and type
        var predicate = base.isTheExpected(stream);
        // add a more specific description for your stream here specifying hostname etc.
        //predicate &= stream.HostName.Equals("Expected Hostname");
        return predicate;
    }

    /// <summary>
    /// Override this method to implement whatever should happen with the samples...
    /// IMPORTANT: Avoid heavy processing logic within this method, update a state and use
    /// coroutines for more complexe processing tasks to distribute processing time over
    /// several frames
    /// </summary>
    /// <param name="newSample"></param>
    /// <param name="timeStamp"></param>
    protected override void Process(float[] newSample, double timeStamp)
    {
        //Assuming that a sample contains at least 3 values for x,y,z
        float x = useX ? newSample[0] : 1;
        float y = useY ? newSample[1] : 1;
        float z = useZ ? newSample[2] : 1;

        // we map the data to the scale factors
        // var targetScale = new Vector3(x, y, z);

        // apply the rotation to the target transform
        // targetTransform.localScale = targetScale;
        // targetText.text = string.Format("hr: {0}bpm\nrr: {1}ms\nstd dev rr: {2}ms", 1, 1, 1);

        Debug.Log(z);
        // sphereSize = new Vector3(x/15, 1, 1);
        sphereColor = new Color((1 - z), 0.3f, z);
    }

    protected override void OnStreamAvailable()
    {
        pullSamplesContinuously = true;
    }

    protected override void OnStreamLost()
    {
        pullSamplesContinuously = false;
    }

    private void Update()
    {
        if (pullSamplesContinuously)
        {
            /*
            interval = interval + 1;
            
            if (interval > 10)
            {
                pullSamples();
                interval = 0;
                // this.transform.localScale = sphereSize;
            }*/
            pullSamples();
            gameObject.GetComponent<Renderer>().material.color = sphereColor;
    

        }
    }
}