import api from "./api";


export async function startAnalysis(projectId) {
  if (!projectId) {
    throw new Error("Project ID is required.");
  }

  const response = await api.post(
    `/analysis/${projectId}/start`
  );

  return response.data;
}


export async function getAnalysis(projectId) {
  if (!projectId) {
    throw new Error("Project ID is required.");
  }

  const response = await api.get(
    `/analysis/${projectId}`
  );

  return response.data;
}