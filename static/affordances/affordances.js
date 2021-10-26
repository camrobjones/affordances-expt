/* === Affordances Experiment === */


// Instructions
var instructions = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Sentence Rating Task
    </h2>
    <p class='instructions'>
      In this task, you will read short passages and rate each passage
      based on how sensible you think it is.
      In particular, focus on whether the action described in the last
      sentence is sensible in the context of the whole passage.
    </p>

    <p class='instructions'>
      Below the passage you will see a 7 point scale for rating the 
      final sentence. The scale goes from 1 (virtual nonsense) to 7
      (completely sensible). Click on the scale to indicate your rating
      and then click the continue button to procede.
    </p>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press the spacebar to begin</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};

// Trial

function affordanceParseResponse(data) {
    // Parse likert response from html
    let responses = JSON.parse(data.responses);
    data.response = responses["affordance-response"];
}


var affordanceTrial = {
  // Post Test Questionnaire
  type: "survey-html-form",
  data: function() {
    return {
        trial_part: 'trial',
        task: 'affordance',
        scale: "SENSIBILITY",
        item_type: "critical",
        item_id: jsPsych.timelineVariable('item_id')(),
        item: jsPsych.timelineVariable('item')(),
        version: jsPsych.timelineVariable('version')(),
        condition: jsPsych.timelineVariable('condition')()
    };
  },

  html: function() {
    let sent = jsPsych.timelineVariable('stimulus')();
    let stimulus = 
        `<div class='question likert affordance'>

            <p class='stimulus likert affordance'>${sent}</p>

            
            <div class='option-container likert'>

                <div class='radio-option likert'>
                    <label for='affordance-response-1' class='radio-label likert'>1</label>
                    <input type='radio' name='affordance-response' id='affordance-response-1'
                    value="1"/ required class='likert'>
                    <label for='affordance-response-1' class='radio-label likert'>
                        Virtual Nonsense
                    </label>
                </div>

                <div class='radio-option likert'>
                    <label for='affordance-response-2' class='radio-label likert'>2</label>
                    <input type='radio' name='affordance-response' id='affordance-response-2'
                    value="2"/ required class='likert'>
                </div>

                <div class='radio-option likert'>
                    <label for='affordance-response-3' class='radio-label likert'>3</label>
                    <input type='radio' name='affordance-response' id='affordance-response-3'
                    value="3"/ required class='likert'>
                </div>

                <div class='radio-option likert'>
                    <label for='affordance-response-4' class='radio-label likert'>4</label>
                    <input type='radio' name='affordance-response' id='affordance-response-4'
                    value="4"/ required class='likert'>
                    
                </div>

                <div class='radio-option likert'>
                    <label for='affordance-response-5' class='radio-label likert'>5</label>
                    <input type='radio' name='affordance-response' id='affordance-response-5'
                    value="5"/ required class='likert'>
                    
                </div>

                <div class='radio-option likert'>
                    <label for='affordance-response-6' class='radio-label likert'>6</label>
                    <input type='radio' name='affordance-response' id='affordance-response-6'
                    value="6"/ required class='likert'>
                    
                </div>

                <div class='radio-option likert'>
                    <label for='affordance-response-7' class='radio-label likert'>7</label>
                    <input type='radio' name='affordance-response' id='affordance-response-7'
                    value="7"/ required class='likert'>
                    <label for='affordance-response-7' class='radio-label likert'>
                        Completely Sensible
                    </label>
                </div>

            </div>

        </div>`;
        return stimulus;
    },
  choices: jsPsych.NO_KEYS,
  post_trial_gap: 500,
  on_finish: function(data) {
    affordanceParseResponse(data);
    updateProgress();
  }
};

// Combine fixation, preview, and trial into one component
var affordanceTrialProcedure = {
  timeline: [affordanceTrial],
  timeline_variables: tasks.affordance
};


// Finish
var finish = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Segment Complete
    </h2>
    <p class='instructions'>
      That concludes the sentence rating segment of the experiment.
      Press the spacebar to continue to the next task.
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};


// Create timeline

if ("affordance" in tasks) {

  var affordanceTimeline = [instructions, affordanceTrialProcedure, finish];

  // Instruction, end, trials
  var affordanceTrialCount = 2 + tasks.affordance.length;

}


