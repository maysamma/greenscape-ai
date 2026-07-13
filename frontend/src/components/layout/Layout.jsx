export default function Card({ children, className = "" }) {
  return (
    <div
      className={`rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition hover:shadow-lg ${className}`}
    >
      {children}
    </div>
  );
}