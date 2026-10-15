import { apiClient } from './client';

export async function registerUserAPI({ matriculation_number, username, password }) {
  return apiClient('/user/register', {
    method: 'POST',
    body: {
      matriculation_number,
      username,
      password,
    },
  });
}
export async function discoverProfileAPI(){
  return apiClient(`/user/discover`,{
    method: 'GET'
  });
}

export async function createProfileAPI() {
  return apiClient(`/user/createProfile`, {
    method: 'POST'
  });
}
export async function loginUserAPI({ matriculation_number, password }) {
  return apiClient('/user/login', {
    method: 'POST',
    body: {
      matriculation_number,
      password,
    },
  });
}
export async function getUserFromCookiesAPI() {
  return apiClient('/user/get_user', {
    method: 'GET',
  });
}

export async function getUserDataAPI(matriculation_number) {
  return apiClient(`/user/me/${matriculation_number}`, {
    method: 'GET',
  });
}

export async function logoutUserAPI() {
  return apiClient('/user/logout', {
    method: 'POST',
  });
}

export async function getUserProfilesAPI() {
  return apiClient('/user/get_profiles', {
    method: 'GET',
  });
}




export async function get_my_created_profilesAPI() {
  return apiClient('/user/my_profile', {
    method: 'GET',
  });
}

export async function get_active_profilesAPI() {
  return apiClient('/user/get_active_profiles', {
    method: 'GET',
  });
}

export async function authStatusAPI() {
  const response = await fetch("/user/auth_status", {
    credentials: "include",
  });

  if (response.status === 401) {
    window.dispatchEvent(
      new Event("sessionExpired")
    );

    throw new Error("Unauthorized");
  }

  return response.json();
}


