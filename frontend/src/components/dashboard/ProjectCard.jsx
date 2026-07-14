import {
  Building2,
  MapPin,
  Layers3,
  Ruler,
} from "lucide-react";

import Card from "../common/Card";

export default function ProjectCard({ project }) {
  return (
    <Card>

      <h2 className="text-2xl font-bold mb-8">
        Project Information
      </h2>

      <div className="space-y-6">

        <div className="flex items-center gap-4">

          <Building2 className="text-green-600" />

          <div>
            <p className="text-sm text-slate-500">
              Project Name
            </p>

            <h3 className="font-semibold">
              {project.name}
            </h3>
          </div>

        </div>

        <div className="flex items-center gap-4">

          <Building2 className="text-green-600" />

          <div>
            <p className="text-sm text-slate-500">
              Building Type
            </p>

            <h3 className="font-semibold">
              {project.building_type}
            </h3>
          </div>

        </div>

        <div className="flex items-center gap-4">

          <MapPin className="text-green-600" />

          <div>
            <p className="text-sm text-slate-500">
              Location
            </p>

            <h3 className="font-semibold">
              {project.location}
            </h3>
          </div>

        </div>

        <div className="flex items-center gap-4">

          <Ruler className="text-green-600" />

          <div>
            <p className="text-sm text-slate-500">
              Floor Area
            </p>

            <h3 className="font-semibold">
              {project.floor_area} m²
            </h3>
          </div>

        </div>

        <div className="flex items-center gap-4">

          <Layers3 className="text-green-600" />

          <div>
            <p className="text-sm text-slate-500">
              Floors
            </p>

            <h3 className="font-semibold">
              {project.floors} Floors
            </h3>
          </div>

        </div>

      </div>

    </Card>
  );
}