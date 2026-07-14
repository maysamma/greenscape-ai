import Card from "../common/Card";
import { CheckCircle2 } from "lucide-react";

const recommendations = [

  "Increase daylight in the living room.",

  "Improve natural ventilation strategy.",

  "Reduce glazing ratio on the west façade.",

  "Use sustainable construction materials.",

  "Optimize wall insulation for better energy efficiency.",

];

export default function RecommendationCard() {

  return (

    <Card>

      <h2 className="text-2xl font-bold mb-8">

        AI Recommendations

      </h2>

      <div className="space-y-5">

        {recommendations.map((item) => (

          <div
            key={item}
            className="flex items-start gap-3"
          >

            <CheckCircle2
              className="text-green-600 mt-1"
              size={20}
            />

            <p className="text-slate-700 leading-7">

              {item}

            </p>

          </div>

        ))}

      </div>

    </Card>

  );

}