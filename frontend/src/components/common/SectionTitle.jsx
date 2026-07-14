export default function SectionTitle({
    title,
    subtitle
}) {
    return (

        <div className="text-center mb-16">

            <p className="text-green-600 font-semibold">

                {subtitle}

            </p>

            <h2 className="text-4xl font-bold mt-3">

                {title}

            </h2>

        </div>

    );
}