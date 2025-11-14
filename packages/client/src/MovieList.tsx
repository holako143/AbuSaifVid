import { useState } from 'react';
import { trpc } from './trpc';

export function MovieList() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [linkUrl, setLinkUrl] = useState('');
  const [linkType, setLinkType] = useState('Download');

  const moviesQuery = trpc.movie.getMovies.useQuery();
  const addMovieMutation = trpc.movie.addMovie.useMutation({
    onSuccess: () => {
      // Invalidate and refetch the movies query to show the new movie
      moviesQuery.refetch();
    },
  });

  const handleAddMovie = () => {
    addMovieMutation.mutate({
      title,
      description,
      links: [{ url: linkUrl, type: linkType }],
    });
    // Clear form
    setTitle('');
    setDescription('');
    setLinkUrl('');
  };

  return (
    <div className="flex flex-col gap-8 p-8 bg-gray-800 rounded-lg">
      <div>
        <h2 className="text-2xl mb-4">Add New Movie</h2>
        <div className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="p-2 bg-gray-700 rounded"
          />
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="p-2 bg-gray-700 rounded"
          />
          <input
            type="text"
            placeholder="Link URL"
            value={linkUrl}
            onChange={(e) => setLinkUrl(e.target.value)}
            className="p-2 bg-gray-700 rounded"
          />
          <input
            type="text"
            placeholder="Link Type (e.g., Download)"
            value={linkType}
            onChange={(e) => setLinkType(e.target.value)}
            className="p-2 bg-gray-700 rounded"
          />
          <button onClick={handleAddMovie} className="p-2 bg-purple-600 rounded hover:bg-purple-700">
            Add Movie
          </button>
          {addMovieMutation.error && <p className="text-red-500">{addMovieMutation.error.message}</p>}
        </div>
      </div>

      <div>
        <h2 className="text-2xl mb-4">Movies</h2>
        {moviesQuery.isLoading && <p>Loading movies...</p>}
        {moviesQuery.error && <p className="text-red-500">{moviesQuery.error.message}</p>}
        <ul className="flex flex-col gap-4">
          {moviesQuery.data?.map((movie) => (
            <li key={movie.id} className="p-4 bg-gray-700 rounded">
              <h3 className="text-xl font-bold">{movie.title}</h3>
              <p>{movie.description}</p>
              <ul className="mt-2">
                {movie.links.map((link) => (
                  <li key={link.id}>
                    <a href={link.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                      {link.type}: {link.url}
                    </a>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
