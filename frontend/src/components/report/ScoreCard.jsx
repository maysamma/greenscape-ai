import Card from "../common/Card";

const scores = [
  {
    title: "Overall Score",
    score: "92%",
  },
  {
    title: "Sustainability",
    score: "91%",
  },
  {
    title: "Energy",
    score: "88%",
  },
  {
    title: "Lighting",
    score: "94%",
  },
  {
    title: "Ventilation",
    score: "90%",
  },
  {
    title: "Accessibility",
    score: "95%",
  },
  {
    title: "Building Code",
    score: "89%",
  },
  {
    title: "Cost Optimization",
    score: "84%",
  },
];

export default function ScoreCard() {
  return (
    <Card>

      <h2 className="text-2xl font-bold mb-8">
        Analysis Scores
      </h2>

      <div className="space-y-5">

        {scores.map((item) => (

          <div key={item.title}>

            <div className="flex justify-between mb-2">

              <span className="font-medium">
                {item.title}
              </span>

              <span className="text-green-600 font-bold">
                {item.score}
              </span>

            </div>

            <div className="w-full bg-slate-200 rounded-full h-3">

              <div
                className="bg-green-600 h-3 rounded-full"
                style={{
                  width: item.score,
                }}
              />

            </div>

          </div>

        ))}

      </div>

    </Card>
  );
}