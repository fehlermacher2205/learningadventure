import { apiClient } from './client';



export async function getProfileAPI(profile_id) {
  return apiClient(`/profiles/${profile_id}`, {
    method: 'GET',
  });
}



export async function editBackgroundAPI(profile_id, background){
  return apiClient(`/profiles/${profile_id}/editbackground`,{
    method: 'PUT',
    body:{
      background
    }
  });
}

export async function editProfileNameAPI(profile_id, profile_name) {
  return apiClient(`/profiles/${profile_id}/editname`, {
    method: "PUT",
    body: {
      profile_name
    }
  });
}
export async function editPromptsAPI(profile_id, new_prompt, prompt_type) {
  return apiClient(`/profiles/${profile_id}/edit_prompts`, {
    method: 'PUT',
    body: {
      new_prompt,
      prompt_type
    },
  });
}


export async function getQuestionWithIDAPI(profile_id, question_id) {
  return apiClient(`/profiles/${profile_id}/get/${question_id}`, {
    method: 'GET',
  });
}

export async function getAllQuestionsAPI(profile_id) {
  return apiClient(`/profiles/${profile_id}/getquestions`, {
    method: 'GET',
  });
}

export async function edit_questionAPI(profile_id, question_text,position) {
  return apiClient(`/profiles/${profile_id}/edit_question`, {
    method: 'PUT',
    body: {
      question_text,
      position
    },
  });
}

export async function add_questionAPI(profile_id, question_text) {
  return apiClient(`/profiles/${profile_id}/add_question`, {
    method: 'POST',
    body: {
      profile_id,
      question_text,
    },
  });
}



export async function remove_questionAPI(profile_id, question_position) {
  return apiClient(`/profiles/${profile_id}/remove_question`, {
    method: 'POST',
    body: {
      profile_id,
      question_position,
    },
  });
}

export async function change_visibility(profile_id, visible) {
  return apiClient(`/profiles/${profile_id}/change_visibility`, {
    method: 'PUT',
    body: {
      visible
    },
  });
}

export async function get_me_activeGoalsAPI(profile_id){
  return apiClient(`/profiles/${profile_id}/my_activeProfile`, {
    method: 'GET',
  });
}

export async function addallgoalsAPI(profile_id){
  return apiClient(`/profiles/${profile_id}/my_add_all`, {
    method: 'POST',
  });
}


















export async function addGoalAPI(profile_id, goalData) {
  return apiClient(`/profiles/${profile_id}/create_predefined_goal`, {
    method: "POST",
    body: {
      title: goalData.title,
      category: goalData.category,
      skill: goalData.skill,
      level: goalData.level,
    },
  });
}

export async function generateGoalAPI(goalData) {
  return apiClient(`/profiles/generateGoal`, {
    method: "POST",
    body: {
      title: goalData.title,
      category: goalData.category,
      skill: goalData.skill,
      level: goalData.level,
    },
  });
}



export async function generateBackgroundStoryAPI(choice_text, profile_id) {
  return apiClient(`/profiles/${profile_id}/generatebackground`, {
    method: 'POST',
    body: {
      choice_text,
      profile_id,
    },
  });
}


export async function getProfileNameAPI(profile_id) {
  return apiClient(`/profiles/${profile_id}/getname`, {
    method: "GET",
  });
}


export async function get_active_storyAPI(profile_id) {
  return apiClient(`/profiles/${profile_id}/get_active_story`, {
    method: 'GET',
  });
}

export async function get_expire_storiesAPI(profile_id) {
  return apiClient(`/profiles/${profile_id}/get_expire_stories`, {
    method: 'GET',
  });
}











export async function changegoalPriorityAPI(profile_id,goal_id ) {
  return apiClient(`/profiles/${profile_id}/my_changegoalPriority`, {
    method: 'PUT',
    body: {
      profile_id,
      goal_id
    },
  });
}
export async function addgoalManualAPI( profile_id,title,category,skill,level,priority) {
  return apiClient(`/profiles/${profile_id}/my_addgoal`, {
    method: 'POST',
    body: {
      profile_id,
      title,
      category,
      skill,
      level,
      priority
    },
  });
}

export async function addonegoalAPI(profile_id,predefinedgoal_id){
  return apiClient(`/profiles/${profile_id}/my_addgoal_predefined`, {
    method: 'POST',
    body: {
      profile_id,
      predefinedgoal_id,
    },
  });
}
export async function removeonegoalAPI(profile_id,goal_id){
  return apiClient(`/profiles/${profile_id}/my_removegoal`, {
    method: 'POST',
    body: {
      profile_id,
      goal_id,
    },
  });
}
