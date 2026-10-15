import { apiClient } from './client';
// please note that this api belong to profile router
// due to story belong to a profile

export async function generateBackgroundStory(story_id, choice_text) {
  return await apiClient(
    `/stories/${story_id}/generatebackground`,
    {
      method: "POST",
      body: {
        choice_text 
      }
    }
  );
}

export async function editStorybackgroundAPI(story_id,background){
  return apiClient(`/stories/${story_id}/editbackground`,{
    method: 'PUT',
    body: {
        background 
      }
  });
}
export async function editsnapshotAPI(story_id,answers_snapshot){
  return apiClient(`/stories/${story_id}/editsnapshot`,{
    method: 'PUT',
    body:{
      answers_snapshot
    }
  });
}
export async function endStoryAPI(story_id){
  return apiClient(`/stories/${story_id}/endstory`,{
    method: 'PUT'
  });
}
export async function getStoryAPI(story_id) {
  return await apiClient(
    `/stories/${story_id}`,
    {
      method: "GET",
    }
  );
}
export async function getActionHistoryAPI(story_id){
  return await apiClient(
    `/stories/${story_id}/action_history`,
    {
      method: "GET",
    }
  );
}

export async function generateNewStoryPageAPI(story_id, choice_text, context_strategy) {
  return await apiClient(
    `/stories/${story_id}/generatepage`,
    {
      method: "POST",
      body: {
        choice_text,
        context_strategy 
      }
    }
  );
}


export async function evaluateLastActionAPI(story_id) {
  return await apiClient(`/stories/${story_id}/action_evaluation`, {
    method: 'POST',
    body: {
      story_id,
    },
  });
}