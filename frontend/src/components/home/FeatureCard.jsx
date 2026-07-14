import Card from "../common/Card";

export default function FeatureCard({
  icon: Icon,
  title,
  description,
}) {
  return (
    <Card
      className="
      h-full
      hover:-translate-y-2
      transition-all
      duration-300
      group
      "
    >
      <div className="bg-green-100 w-14 h-14 rounded-xl flex items-center justify-center mb-6 group-hover:bg-green-600 transition">

        <Icon
          className="text-green-600 group-hover:text-white"
          size={28}
        />

      </div>

      <h3 className="text-xl font-bold mb-4">

        {title}

      </h3>

      <p className="text-slate-500 leading-7">

        {description}

      </p>

    </Card>
  );
}