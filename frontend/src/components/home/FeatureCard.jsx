import Card from "../common/Card";

export default function FeatureCard({
  icon,
  title,
  description,
}) {
  return (
    <Card>

      <div className="text-4xl">
        {icon}
      </div>

      <h3 className="mt-5 text-xl font-semibold">
        {title}
      </h3>

      <p className="mt-3 text-gray-500">
        {description}
      </p>

    </Card>
  );
}