export default function BigButton({text, onClick}) {
  return (
    <button
      className="w-64 h-12 bg-white hover:bg-gray-300 text-gray-700 rounded-full 
            shadow-lg hover:shadow-xl transition duration-300 ease-in-out"
      onClick={onClick}
    >
      {text}
    </button>
  );
}
