"""
Views for Glenberg & Robertson (2000) replication.

-----

"""
import os
import json
import random
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone as tz
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from affordances.models import (Participant, Rating, BinaryChoice,
                                FreeResponse)
from affordances.secrets import SONA_EXPT_ID, SONA_CREDIT_TOKEN

"""
Parameters
----------
"""

# General parameters
MODULE_NAME = "affordances"
RESULTS_DIR = MODULE_NAME + '/data/results/'  # Store responses

RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"
SONA_URL = "https://ucsd.sona-systems.com/services/SonaAPI.svc/WebstudyCredit"

MODELS = {
    "participant": Participant,
    "rating": Rating,
    "binary": BinaryChoice,
    "free": FreeResponse
}


"""
Load Data
---------
Helper functions to load and reformat data.
"""


def load_affordance_sentences(limit=None):
    """Load the sentences from G&R 2000 for rating."""
    df = pd.read_csv("affordances/data/affordance_sentences.csv")

    # Select version for each id randomly
    item_ids = df['item'].unique()  # Get unique ids
    random.shuffle(item_ids)  # Randomly shuffle
    aff, naf, rel = np.split(item_ids, 3)  # Split into 3

    # Select and concatenate item versions
    items = pd.concat([
        df.loc[(df["item"].isin(aff)) & (df["condition"] == "afforded")],
        df.loc[(df["item"].isin(naf)) & (df["condition"] == "nonafforded")],
        df.loc[(df["item"].isin(rel)) & (df["condition"] == "related")]
    ])

    # Randomly shuffle
    items = items.sample(frac=1)

    # Limit
    items = items[:limit]

    # Convert to JSON-style record dict
    items = items.to_dict(orient="records")

    return items


def load_irq(limit=None):
    """Load the IRQ rating statements.

    Note: limiting will not guarantee filler q's are sampled
    """
    df = pd.read_csv("affordances/data/irq.csv")  # Load
    df = df.sample(frac=1)  # Randomly shuffle
    df = df[:limit]  # Limit
    items = df.to_dict(orient="records")  # Convert to JSON-style record dict

    return items


def load_mr(limit=15, fillers=3):
    """Load the Mental Rotation stimuli."""
    limit = 47 if limit is None else limit

    # Select limit ids
    item_indices = random.choices(range(2, 49), k=limit)

    # For each id, select reversed & rotation
    items = []
    for item_index in item_indices:

        # Randomly sample parameters
        reversed_flag = random.choice([True, False])
        if reversed_flag:
            rotation = random.choice([0, 50, 100, 150])
        else:
            rotation = random.choice([50, 100, 150])  # No 0 rotation matches

        # Create item id
        item_id = f"{item_index}_{rotation}"

        correct_response = True
        if reversed_flag:
            item_id += "_R"  # Append flag to item id
            correct_response = False  # Not the same object

        # Generate image filepath
        path = f"static/affordances/mental_rotation/{item_id}.jpg"

        items.append({
            "item": item_index,
            "item_type": "critical",
            "reversed": reversed_flag,
            "rotation": rotation,
            "item_id": item_id,
            "correct_response": correct_response,
            "path": path
            })

    # Create fillers (not reversed, 0 rotation)
    filler_indices = random.choices(range(2, 49), k=fillers)
    for item_index in filler_indices:

        # Create item id
        item_id = f"{item_index}_0"

        items.append({
            "item": item_index,
            "item_type": "filler",
            "reversed": False,
            "rotation": 0,
            "item_id": item_id,
            "correct_response": True,
            "path": f"static/affordances/mental_rotation/{item_id}.jpg"
            })

    # Randomly assign fillers
    random.shuffle(items)

    return items


def load_au():
    """Load stimuli for AU task."""
    return [
        {
            "item": 1,
            "item_id": "1_paperclip",
            "item_type": "critical",
            "condition": "paperclip",
            "stimulus": "A Paperclip",
            "version": ""
        }
    ]


def load_task_data(affordance_limit=None, irq_limit=None, mr_limit=15,
                   au_limit=None):
    """Load stimuli for all tasks.

    Don't include a task if limit == 0
    """
    stimuli = {}

    # Affordances
    if affordance_limit is None or affordance_limit > 0:
        stimuli["affordance"] = load_affordance_sentences(
            limit=affordance_limit)

    # IRQ
    if irq_limit is None or irq_limit > 0:
        stimuli["irq"] = load_irq(limit=irq_limit)

    # MR
    if mr_limit is None:
        mr_limit = 15  # lazy default of 15
    if mr_limit > 0:
        stimuli["mr"] = load_mr(limit=mr_limit)

    # AU (include or exclude task)
    if au_limit is None or au_limit > 0:
        stimuli["au"] = load_au()

    return stimuli


"""
Store Data
----------
"""


def save_json_results(data):
    """Save raw json results as a backup in case something goes wrong..."""
    # Generate filename
    timestamp = tz.now().strftime("%Y-%m-%d-%H-%M-%S")
    ppt_id = data.get('ppt_id')
    filename = f"{timestamp}-{ppt_id}.json"
    filepath = os.path.join(RESULTS_DIR, filename)

    # Ensure RESULTS_DIR exists
    if not os.path.isdir(RESULTS_DIR):
        os.mkdir(RESULTS_DIR)

    # Write file
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

    return True


def store_rating_results(data, ppt):
    """Store results from rating trials."""
    trials = [item for item in data
              if item.get('task') in ["affordance", "irq"]]

    for trial_data in trials:

        print(trial_data)

        rating = Rating.objects.create(
            # Scale & ppt
            participant=ppt,
            scale=trial_data.get('scale'),

            # Item identifier
            item=trial_data.get('item'),
            item_id=trial_data.get('item_id'),
            item_type=trial_data.get('item_type'),
            version=trial_data.get('version', ""),
            condition=trial_data.get('condition', ""),
            trial_index=trial_data.get('trial_index'),

            # Response info
            response=trial_data.get('response'),
            reaction_time=trial_data.get('rt')
        )

        rating.save()


def store_binary_results(data, ppt):
    """Store results from rating trials."""
    trials = [item for item in data
              if item.get('task') == "MR"]

    for trial_data in trials:

        print(trial_data)

        rating = BinaryChoice.objects.create(
            # Scale & ppt
            participant=ppt,
            task=trial_data.get('task'),

            # Item identifier
            item=trial_data.get('item'),
            item_id=trial_data.get('item_id'),
            item_type=trial_data.get('item_type'),
            version=trial_data.get('version', ""),
            condition=trial_data.get('condition', ""),
            trial_index=trial_data.get('trial_index'),

            # Response info
            key_press=trial_data.get('key_press'),
            response=trial_data.get('response'),
            correct_response=trial_data.get('correct_response'),
            is_correct=trial_data.get('is_correct'),
            reaction_time=trial_data.get('rt')
        )

        rating.save()


def store_free_response_results(data, ppt):
    """Store results from rating trials."""
    trials = [item for item in data
              if item.get('task') == "AU"]

    for trial_data in trials:

        print(trial_data)

        rating = FreeResponse.objects.create(
            # Scale & ppt
            participant=ppt,
            task=trial_data.get('task'),

            # Item identifier
            item=trial_data.get('item'),
            item_id=trial_data.get('item_id'),
            item_type=trial_data.get('item_type'),
            version=trial_data.get('version', ""),
            condition=trial_data.get('condition', ""),
            trial_index=trial_data.get('trial_index'),

            # Response info
            response=trial_data.get('response'),
            reaction_time=trial_data.get('rt')
        )

        rating.save()


def store_demographics(data, ppt):
    """Store demographics information."""
    demo = [item for item in data if item.get('trial_part') == "demographics"]

    demo = demo[0]
    demo_data = json.loads(demo.get('responses', "{}"))
    ppt.birth_year = demo_data.get('demographics_year') or None
    ppt.gender = demo_data.get('demographics_gender')
    ppt.native_english = demo_data.get('demographics_english') == "yes"

    ppt.save()


def check_credit_granted(sona_response):
    """Parse SONA XML response and check if credit granted."""
    sona = "http://schemas.datacontract.org/2004/07/emsdotnet.sonasystems"
    namespace = {"sona": sona}

    try:
        root = ET.fromstring(sona_response)
        result = root[0].find("sona:Result", namespace)
        credit_granted = result.find("sona:credit_status", namespace).text
        if credit_granted == "G":
            return True

    except:
        pass

    return False


def store_debrief(data, ppt):
    """Store debrief information."""
    debrief = filter(lambda x: x.get('trial_part') == "post_test", data)

    for debrief_item in debrief:
        debrief_data = json.loads(debrief_item.get('responses', "{}"))
        for name, response in debrief_data.items():
            setattr(ppt, name, response)

    ppt.save()


def save_results(request):
    """Save results to db."""
    # Get posted data
    post = json.loads(request.body.decode('utf-8'))

    # Save raw json
    save_json_results(post)

    # Retreieve ppt
    ppt_id = post.get('ppt_id')
    ppt = Participant.objects.get(pk=ppt_id)

    # store results
    data = post['results']
    store_rating_results(data, ppt)
    store_binary_results(data, ppt)
    store_free_response_results(data, ppt)
    store_demographics(data, ppt)
    store_debrief(data, ppt)

    ppt.end_time = tz.now()

    status = {"success": True}

    print(ppt.SONA_code)

    # Grant credit
    if ppt.SONA_code != "":

        # Build SONA Web Credit URL
        params = {
            'experiment_id': SONA_EXPT_ID,
            'credit_token': SONA_CREDIT_TOKEN,
            'survey_code': ppt.SONA_code}
        url = f"SONA_URL?{urlencode(params)}"

        # Send request & parse content
        response = requests.get(url)
        content = response.content.decode()
        ppt.notes = ppt.notes + f"SONA credit response:\n{content}\n"

        if check_credit_granted(content):
            status["credit"] = "Granted"
        else:
            status["success"] = False
            status["credit"] = "Not granted"

    ppt.save()

    # Notify User
    return JsonResponse(status)


"""
Run Experiment
--------------
"""


def init_ppt(request):
    """Create new ppt."""
    # Get params
    sona_code = request.GET.get('code', "")

    # Get IP Address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR', "")

    # Create DB object
    ppt = Participant.objects.create(
        ip_address=ip_address, SONA_code=sona_code)

    return ppt


def parse_limit(request, arg):
    """Parse string for limit arg."""
    limit = request.GET.get(arg) or None
    limit = int(limit) if limit else None
    return limit


def parse_limits(request):
    """Parse all stimuli limits."""
    limits = {}
    for arg in ["affordance", "irq", "mr", "au"]:
        limits[f"{arg}_limit"] = parse_limit(request, arg)
    return limits


def expt(request):
    """Return experiment view.

    GET Args:
        n (int): Max no. experimental items
        mode (str): Key for experiment type
        fillers (bool): Flag. Include fillers?
    """
    # Create ppt
    ppt = init_ppt(request)

    # Get experimental items
    limits = parse_limits(request)
    tasks = load_task_data(**limits)

    # Create view context
    conf = {"ppt_id": ppt.id}
    context = {"tasks": tasks, "conf": conf}

    # Return view
    return render(request, MODULE_NAME + '/expt.html', context)


def error(request):
    """Error page."""
    return render(request, MODULE_NAME + '/error.html')


def ua_data(request):
    """Store ppt ua_data.

    We do this asynchronously so we can get the fullscreen size
    """
    post = json.loads(request.body.decode('utf-8'))

    ppt_id = post['ppt_id']

    ppt = Participant.objects.get(pk=ppt_id)
    ppt.ua_header = post.get('ua_header', "")
    ppt.screen_width = post.get('width', "")
    ppt.screen_height = post.get('height', "")
    ppt.save()

    return JsonResponse({"success": True})


def validate_captcha(request):
    """Validate captcha token."""
    post = json.loads(request.body.decode('utf-8'))

    ppt_id = post['ppt_id']
    token = post.get('token')

    data = {"response": token,
            "secret": settings.CAPTCHA_SECRET_KEY}

    response = requests.post(RECAPTCHA_URL, data=data)

    content = response.content

    response_data = json.loads(content)

    score = response_data.get('score')
    ppt = Participant.objects.get(pk=ppt_id)
    ppt.captcha_score = score
    ppt.save()

    return JsonResponse(response_data)


"""
Download Data
-------------
"""


def is_admin(user):
    """Check if user is an admin."""
    return user.is_superuser


def get_model_data(model_name):
    """Get data on all trials."""
    model = MODELS[model_name]

    data_list = []
    for record in model.objects.all():

        data = record.__dict__
        data.pop('_state')

        data_list.append(data)

    df = pd.DataFrame(data_list)
    df = df.sort_values('id').reset_index(drop=True)
    return df


@user_passes_test(is_admin)
def download_data(request, model):
    """Download csv of model data."""
    data = get_model_data(model)

    fname = f'pipr_{model}_{tz.now():%Y-%m-%d-%H-%M-%S}.csv'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{fname}"'

    data.to_csv(response, index=False)

    return response
