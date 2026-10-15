import { API_BASE_URL } from "../util";

export async function apiClient(endpoint, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      method: options.method || "GET",
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      credentials: "include",
      ...(options.body && {
        body: JSON.stringify(options.body),
      }),
    }
  );

  let data = null;

  try {
    data = await response.json();
  } catch { 
    // ignore non-json responses
  }

  if (response.status === 401) {
    window.dispatchEvent(
      new Event("sessionExpired")
    );

    window.dispatchEvent(
      new Event("authChanged")
    );

    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    throw new Error(
      data?.detail || "API request failed"
    );
  }

  return data;
}