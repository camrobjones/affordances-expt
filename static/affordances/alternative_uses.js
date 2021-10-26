/* === Alternative Uses Task === */


// Instructions
var instructions = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Alternative Uses Task
    </h2>
    <p class='instructions'>
      In this task, you need to come up with alternative uses for a
      common object.
    </p>

    <p class='instructions'>
      When you begin the task, the name of the common object will
      appear at the top of the screen. Please enter all of the
      alternative uses you can think of for the object in the text box
      below, separated by commas. You will have one minute to list
      all of the uses you can think of.
    </p>

    <p class='instructions'>
      Be inventive and try to think of a diverse range of unusual uses
      for which the object would be appropriate. You don't have to write in full
      sentences, just give enough information to make it clear what the
      intended use is.
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

// Example
var example = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Example
    </h2>
    <p class='instructions'>
      For example, if the object was 'a brick', you might enter the
      following uses in the textbox like so:
    </p>

    <div class='question au'>

      <div class='au-header'>
        <div class='quesiton-title-container'>
          <h3 class='question-title'>
            A Brick
          </h3>
        </div>

        <div class='countdown-container'>
          <span id="countdown-label">Time Remaining:</span><span id="countdown">1:00</span>
        </div>

      </div>

      <textarea class="textbox au" id="au-response" 
      name="au-response" readonly>doorstop, paperweight, bookend, laptop stand, medicine ball, cracking nuts, support for sawing wood, practice retrieving objects from a swimming pool
      </textarea>

    </div>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Your time will start on the next page.
      Press the spacebar to begin.</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};


// Trial

function auParseResponse(data) {
    // Parse likert response from html
    let responses = JSON.parse(data.responses);
    data.response = responses["au-response"];
}

function updateCountdown(remaining) {
  let countdown = document.getElementById("countdown");
  let minutes = Math.floor(remaining / 60);
  let seconds = remaining % 60;
  seconds = String(seconds).padStart(2, '0');
  let countdownString = `${minutes}:${seconds}`;
  countdown.innerText = countdownString;
}

function initCountdown(total) {
  // Set startTime
  let startTime = Date.now();

  // Disable continue Button
  updateCountdown(total);

  // Don't let ppt continue until timer finishes
  let nextBtn = document.getElementById("jspsych-survey-html-form-next");
  nextBtn.disabled = true;

  // Call progressCountdown in 500ms
  setTimeout(function() {progressCountdown(startTime, total);}, 500);

}

function progressCountdown(startTime, total) {
  let timeNow = Date.now();
  let elapsed = (timeNow - startTime) / 1000;  // In seconds
  let remaining = Math.round(total - elapsed);

  if (remaining > 0) {
    updateCountdown(remaining);

    // Call self in 500ms
    setTimeout(function() {progressCountdown(startTime, total);}, 500);
  } else {
    // End trials
    updateCountdown(0);
    let nextBtn = document.getElementById("jspsych-survey-html-form-next");
    nextBtn.disabled = false;

    let auResponse = document.getElementById("au-response");
    auResponse.readOnly = true;
  }
}


var auTrial = {
  // Post Test Questionnaire
  type: "survey-html-form",
  data: function() {
    return {
        trial_part: 'trial',
        task: 'AU',
        item_id: jsPsych.timelineVariable('item_id')(),
        item: jsPsych.timelineVariable('item')(),
        item_type: jsPsych.timelineVariable('item_type')(),
        condition: jsPsych.timelineVariable('condition')(),
        version: jsPsych.timelineVariable('version')(),

    };
  },

  html: function() {
    let object = jsPsych.timelineVariable('stimulus')();
    let stimulus = 
        `<div class='question au'>

          <div class='au-header'>
            <div class='quesiton-title-container'>
              <h3 class='question-title'>
                ${object}
              </h3>
            </div>

            <div class='countdown-container'>
              <span id="countdown-label">Time Remaining:</span><span id="countdown">1:00</span>
            </div>

          </div>

          <textarea class="textbox au" id="au-response" 
          name="au-response"></textarea>

          <input type="hidden" id="hidden-input" name="au-response-hidden"/>

        </div>`;
        return stimulus;
    },
  choices: jsPsych.NO_KEYS,
  post_trial_gap: 500,
  on_load: function() {initCountdown(60)},
  on_finish: function(data) {
    auParseResponse(data);
    updateProgress();
  }
};

// Combine fixation, preview, and trial into one component
var auTrialProcedure = {
  timeline: [auTrial],
  timeline_variables: tasks.au
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
      Press the spacebar to continue.
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};


// Create timeline
if ("au" in tasks) {

  var auTimeline = [instructions, example, auTrialProcedure, finish];

  // Instruction, end, trials
  var auTrialCount = 3 + tasks.au.length;

}
