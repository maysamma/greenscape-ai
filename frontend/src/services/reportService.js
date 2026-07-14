import api from "./api";

export async function getReport(projectId) {
  const response = await api.get(
    `/report/${projectId}`
  );

  return response.data;
}

export async function downloadReport(projectId) {
  const response = await api.get(
    `/report/${projectId}/download`,
    {
      responseType: "blob",
    }
  );

  return response.data;
}