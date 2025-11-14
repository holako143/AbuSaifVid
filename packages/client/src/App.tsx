import { Auth } from './Auth';

function App() {
  return (
    <div className="bg-gray-900 text-white min-h-screen flex items-center justify-center">
      <div className="flex flex-col gap-8">
        <h1 className="text-4xl text-center">React 19 + Tailwind CSS 4 + tRPC</h1>
        <Auth />
      </div>
    </div>
  );
}

export default App;
