import Card from "../common/Card";
import { TriangleAlert } from "lucide-react";

const issues = [

  "Poor daylight in bedroom.",

  "West façade receives excessive heat.",

  "Ventilation can be improved.",

];

export default function IssuesCard() {

  return (

    <Card>

      <h2 className="text-2xl font-bold mb-6">

        Detected Issues

      </h2>

      <div className="space-y-5">

        {issues.map(issue => (

          <div
            key={issue}
            className="flex gap-3"
          >

            <TriangleAlert
              className="text-yellow-500 mt-1"
            />

            <span>

              {issue}

            </span>

          </div>

        ))}

      </div>

    </Card>

  );

}