import Card from "../common/Card";

export default function OverallScoreCard() {
  return (
    <Card className="text-center">

      <p className="text-slate-500">
        Overall Score
      </p>

      <div className="w-44 h-44 border-[14px] border-green-600 rounded-full flex items-center justify-center mx-auto mt-8">

        <div>

          <h1 className="text-6xl font-bold">
            92
          </h1>

          <p className="text-green-600 font-semibold">
            Excellent
          </p>

        </div>

      </div>

    </Card>
  );
}