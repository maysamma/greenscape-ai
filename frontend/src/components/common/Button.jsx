export default function Button({
  children,
  className = "",
  onClick,
}) {
  return (
    <button
      onClick={onClick}
      className={`px-6 py-3 rounded-xl font-semibold transition-all duration-300 ${className}`}
    >
      {children}
    </button>
  );
}