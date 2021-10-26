/* === IRQ Task === */


// Instructions
var instructions = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Object Matching Task
    </h2>
    <p class='instructions'>
      In this task, you will see images of two objects side-by-side.
      Sometimes, the image on the right will show the same object as
      the image on the left but from a different angle. In this case,
      the object on the right could be rotated to match the image on
      the left. In other cases, the images will show different objects,
      so that the objects cannot be rotated to match. Your task is to
      decide whether or not the objects are the same (i.e. they can
      be rotated to match).
    </p>

    <p class='instructions'>
      Use the keyboard to give your answer.
      If the objects can be rotated to match, press the
      <span class='key-demo'>j</span> key. If they can't, press the
      <span class='key-demo'>f</span> key.
      Try to respond as quickly and accurately as possible.
    </p>


    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press the spacebar to continue to an example.</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};

// Instructions
var example_1 = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Object Matching Task | Example 1
    </h2>
    <p class='instructions'>
      For example, if you saw the following pair of objects, 
      you would press <span class='key-demo'>j</span> key, because
      the objects can be rotated to match.
    </p>

    <div class='mr-img-container'>
      <img class="mr-img" src="/static/affordances/mental_rotation/1_50.jpg">
    </div>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press the spacebar to continue.</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};

// Instructions
var example_2 = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Object Matching Task | Example 2
    </h2>
    <p class='instructions'>
      However, in this example, the objects cannot be rotated to match, 
      so you would press the <span class='key-demo'>f</span> key.
    </p>

    <div class='mr-img-container'>
      <img class="mr-img" src="/static/affordances/mental_rotation/1_0_R.jpg">
    </div>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press the spacebar to continue.</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};


// Instructions
var pre_trial = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Begin Task
    </h2>

    <p class='instructions c'>
      The task will begin on the next page.
    </p>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press the spacebar to continue.</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};


// Trial
function mrParseResponse(data) {
  data["response"] = data["key_press"] == 74;  // key press == 'j'
  data["is_correct"] = data["response"] == data["correct_response"];
}


var mrTrial = {
  // Post Test Questionnaire
  type: "html-keyboard-response",
  data: function() {
    return {
        trial_part: 'trial',
        task: 'MR',
        item_id: jsPsych.timelineVariable('item_id')(),
        item: jsPsych.timelineVariable('item')(),
        item_type: jsPsych.timelineVariable('item_type')(),
        condition: jsPsych.timelineVariable('reversed')(),
        version: jsPsych.timelineVariable('rotation')(),
        correct_response: !jsPsych.timelineVariable('reversed')()
    };
  },

  stimulus: function() {
    let path = jsPsych.timelineVariable('path')();
    let stimulus = 
        `<div class='mr-container'>

           <div class='mr-img-container'>
              <img class="mr-img" src="/${path}">
           </div>

           <div class='mr-keyhint-container'>

              <div class='mr-keyhint'>
                <p class='mr-keyhint-label'>
                  No match: <span class='key-demo'>f</span>
                </p>
              </div>

              <div class='mr-keyhint'>
                <p class='mr-keyhint-label'>
                  Match: <span class='key-demo'>j</span>
                </p>
              </div>

           </div>

        </div>`;
        return stimulus;
    },
  choices: ["j", "f"],
  post_trial_gap: 500,
  on_finish: function(data) {
    updateProgress();
    mrParseResponse(data);
  }
};

// Combine fixation, preview, and trial into one component
var mrTrialProcedure = {
  timeline: [mrTrial],
  timeline_variables: tasks.mr
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
      That concludes this segment of the experiment.
      Press the spacebar to continue to the next segment.
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};


// Create timeline

if ("mr" in tasks) {

  var mrTimeline = [instructions, example_1, example_2, pre_trial,
                    mrTrialProcedure, finish];

  // Instruction, end, trials
  var mrTrialCount = 5 + tasks.mr.length;

}

