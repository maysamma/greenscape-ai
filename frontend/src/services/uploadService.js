import api from "./api";


export async function uploadFloorPlan(
  selectedFile,
  projectInfo
) {
  if (!selectedFile) {
    throw new Error(
      "A floor plan file is required."
    );
  }

  const formData = new FormData();

  formData.append(
    "file",
    selectedFile
  );

  formData.append(
    "project_name",
    projectInfo.project_name
  );

  formData.append(
    "building_type",
    projectInfo.building_type
  );

  formData.append(
    "location",
    projectInfo.location
  );

  formData.append(
    "orientation",
    projectInfo.orientation || "North"
  );

  formData.append(
    "area",
    String(projectInfo.area || 0)
  );

  formData.append(
    "floors",
    String(projectInfo.floors || 1)
  );

  const response = await api.post(
    "/upload",
    formData
  );

  return response.data;
}