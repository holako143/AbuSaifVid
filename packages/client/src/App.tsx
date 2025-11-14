import { MovieList } from './MovieList';
// import { Auth } from './Auth';

function App() {
  return (
    <div className="bg-gray-900 text-white min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl text-center mb-8">Movie Link Manager</h1>
        <MovieList />
        {/* <Auth /> */}
      </div>
    </div>
  );
}

export default App;
