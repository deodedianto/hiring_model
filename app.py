import flask
import urllib.request
import json
import os
import ssl

app = flask.Flask(__name__, template_folder='templates')
@app.route('/')
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        def allowSelfSignedHttps(allowed):
            if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                ssl._create_default_https_context = ssl._create_unverified_context

        allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
        data = {
            "Inputs": {
                "WebServiceInput0":
                [
                    {
                        'Segment': "Young & Searching",
                        'Stability': "0.57",
                        'Trustworthiness / Integrity': "0.69",
                        'Coachability': "0.6",
                        'Self Evaluation Score for the Job': "6",
                    },
                ],
             },
            "GlobalParameters": {
            }
        }
        new=data['Inputs']['WebServiceInput0']
        new=dict(new[0])

        body = str.encode(json.dumps(data))
        url = 'http://f932e94a-b12c-48d6-9d0c-e92a88a9bc0a.centralus.azurecontainer.io/score'
        api_key = 'mSNspYilm0uDHa0mXAteCXvIyV0AvedH' # Replace this with the API key for the web service
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)
        result = response.read()
        pred=json.loads(result)
        pred=pred['Results']['output1']
        pred=dict(pred[0])

    
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'Segment':new['Segment'],
                                                     'Stability':new['Stability'],
                                                     'Trustworthiness / Integrity':new['Trustworthiness / Integrity'],
                                                     'Coachability':new['Coachability'],
                                                     'Self Evaluation Score for the Job':new['Self Evaluation Score for the Job']},
                                     result=pred['Should Hire Prediction'],
                                     )
    return(flask.render_template('main.html'))
if __name__ == '__main__':
    app.run()