using System.Collections;
using UnityEngine;
using Assets.LSL4Unity.Scripts;
using Assets.LSL4Unity.Scripts.AbstractInlets;

public class museTest : InletFloatSamples
{
    public Vector3 concValue = new Vector3(1, 1, 1);
    
    public bool useX;
    public bool useY;
    public bool useZ;

    private bool pullSamplesContinuously = false;
    private int interval = 0;


    void Start()
    {
        // [optional] call this only, if your gameobject hosting this component
        // got instantiated during runtime
        Debug.Log("start muse");

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
        float conc = useX ? newSample[21] : 1;
        float mellow = useY ? newSample[20] : 1;

        Debug.Log("conc: " + conc + "; mellow: " + mellow);

        // we map the data to the scale factors
        // var targetScale = new Vector3(x, y, z);

        // apply the rotation to the target transform
        // targetTransform.localScale = targetScale;
        // targetText.text = string.Format("hr: {0}bpm\nrr: {1}ms\nstd dev rr: {2}ms", 1, 1, 1);
        concValue = new Vector3(conc*10, mellow*10, 5);
        // sphereSize.x = x;
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
            interval = interval + 1;

            if (interval > 10)
            {
                pullSamples();
                interval = 0;
                this.transform.localScale = concValue;

                //Fetch the Renderer from the GameObject
                Renderer rend = GetComponent<Renderer>();

                //Set the main Color of the Material to green
                rend.material.shader = Shader.Find("_Color");
                rend.material.SetColor("_Color", Color.green);
            }

        }
    }
}