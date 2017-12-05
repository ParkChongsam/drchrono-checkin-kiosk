
Survey.Survey.cssType = "bootstrap";
Survey.defaultBootstrapCss.navigationButton = "btn btn-green";

window.survey = new Survey.Model({
 "pages": [
  {
   "name": "page1",
   "elements": [
    { "type": "rating", "name": "satisfaction", "title": "How satisfied are you with the Kiosk?", "mininumRateDescription": "Not Satisfied", "maximumRateDescription": "Completely satisfied" },
    {
     "type": "panel", "innerIndent": 1, "name": "panel1", "title": "Please, help us improve our Kiosk", "visibleIf": "{satisfaction} < 3",
     "elements": [
        { "type": "checkbox", "choices": [ { "value": "1", "text": "User Friendliness / Flexibility" }, { "value": "2", "text": "Page Request is taking too long" }, { "value": "3", "text": "Other" } ], "name": "What should be improved?" },
        { "type": "comment", "name": "suggestions", "title":"What would make you more satisfied with the Kiosk?" }
     ]
    }
   ]
  }
 ]
});
survey.data = {satisfaction: 2};

survey.onComplete.add(function(result) {
	document.querySelector('#surveyResult').innerHTML = "result: " + JSON.stringify(result.data);
});


$("#surveyElement").Survey({model:survey});

