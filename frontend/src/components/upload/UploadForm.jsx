import Card from "../common/Card";

export default function UploadForm({
  projectInfo,
  setProjectInfo,
}) {

  function handleChange(e) {
    const {
      name,
      value,
      type,
    } = e.target;

    setProjectInfo((prev) => ({
      ...prev,
      [name]:
        type === "number"
          ? Number(value)
          : value,
    }));
  }

  return (

    <Card>

      <h2 className="text-2xl font-bold mb-8">
        Project Information
      </h2>

      <div className="grid md:grid-cols-2 gap-6">

        <div>

          <label className="block mb-2 font-medium">
            Project Name
          </label>

          <input
            type="text"
            name="project_name"
            value={projectInfo.project_name}
            onChange={handleChange}
            placeholder="Green Residence"
            className="w-full rounded-xl border border-slate-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
          />

        </div>

        <div>

          <label className="block mb-2 font-medium">
            Building Type
          </label>

          <select
            name="building_type"
            value={projectInfo.building_type}
            onChange={handleChange}
            className="w-full rounded-xl border border-slate-300 p-3"
          >

            <option value="Residential">
              Residential
            </option>

            <option value="Commercial">
              Commercial
            </option>

            <option value="Hospital">
              Hospital
            </option>

            <option value="School">
              School
            </option>

            <option value="Office">
              Office
            </option>

          </select>

        </div>

        <div>

          <label className="block mb-2 font-medium">
            Location
          </label>

          <input
            type="text"
            name="location"
            value={projectInfo.location}
            onChange={handleChange}
            placeholder="Makkah"
            className="w-full rounded-xl border border-slate-300 p-3"
          />

        </div>

        <div>

          <label className="block mb-2 font-medium">
            Floor Area (m²)
          </label>

          <input
            type="number"
            name="area"
            min="1"
            value={projectInfo.area}
            onChange={handleChange}
            placeholder="450"
            className="w-full rounded-xl border border-slate-300 p-3"
          />

        </div>
        <div>
          <label className="block mb-2 font-medium">
            Number of Floors
          </label>

          <input
            type="number"
            name="floors"
            min="1"
            value={projectInfo.floors}
            onChange={handleChange}
            className="w-full rounded-xl border border-slate-300 p-3"
          />
        </div>

        <div>

          <label className="block mb-2 font-medium">
            Orientation
          </label>

          <select
            name="orientation"
            value={projectInfo.orientation}
            onChange={handleChange}
            className="w-full rounded-xl border border-slate-300 p-3"
          >

            <option value="North">
              North
            </option>

            <option value="South">
              South
            </option>

            <option value="East">
              East
            </option>

            <option value="West">
              West
            </option>

          </select>

        </div>

      </div>

    </Card>

  );

}