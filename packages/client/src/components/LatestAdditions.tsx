import { useState } from 'react';

interface Server {
  name: string;
  quality: string;
  url: string;
}

interface CardData {
  id: number;
  imageUrl: string;
  title: string;
  category: string;
  episode?: number;
  servers: Server[];
}

const dummyData: CardData[] = [
  {
    id: 1,
    imageUrl: 'https://via.placeholder.com/300x450',
    title: 'فيلم الأكشن الجديد',
    category: 'أفلام أجنبية',
    servers: [
      { name: 'سيرفر 1', quality: '1080p', url: '#' },
      { name: 'سيرفر 2', quality: '720p', url: '#' },
    ],
  },
  {
    id: 2,
    imageUrl: 'https://via.placeholder.com/300x450',
    title: 'مسلسل الدراما',
    category: 'مسلسلات تركية',
    episode: 5,
    servers: [
      { name: 'سيرفر 1', quality: '1080p', url: '#' },
      { name: 'سيرفر 2', quality: '720p', url: '#' },
      { name: 'سيرفر 3', quality: '480p', url: '#' },
    ],
  },
  // Add more dummy data as needed...
];

export const LatestAdditions = () => {
  const [expandedCardId, setExpandedCardId] = useState<number | null>(null);
  const duplicatedData = [...dummyData, ...dummyData, ...dummyData];

  const handleCardClick = (id: number) => {
    setExpandedCardId(expandedCardId === id ? null : id);
  };

  return (
    <div className="relative w-full overflow-hidden my-8">
      <div className="flex animate-scroll group">
        {duplicatedData.map((item, index) => (
          <div
            key={`${item.id}-${index}`}
            className={`flex-shrink-0 w-64 bg-gray-800 rounded-lg mx-4 cursor-pointer overflow-hidden transform transition-all duration-500 ${
              expandedCardId === item.id ? 'scale-110' : 'hover:scale-105'
            }`}
            onClick={() => handleCardClick(item.id)}
          >
            <div className="relative">
              <img src={item.imageUrl} alt={item.title} className="w-full h-96 object-cover" />
              <div className="absolute inset-0 bg-black bg-opacity-50 flex items-end p-4 opacity-0 transition-opacity duration-300 hover:opacity-100">
                <h3 className="text-xl font-bold">{item.title}</h3>
              </div>
              {item.episode && (
                <div className="absolute top-2 right-2 bg-red-600 text-white text-sm font-bold px-2 py-1 rounded">
                  الحلقة {item.episode}
                </div>
              )}
            </div>
            <div className="p-4 text-right">
              <p className="text-gray-400">{item.category}</p>
            </div>
            {expandedCardId === item.id && (
              <div className="p-4 bg-gray-700">
                <h4 className="text-lg font-bold mb-2">سيرفرات التحميل</h4>
                <ul className="space-y-2">
                  {item.servers.map((server) => (
                    <li key={server.name}>
                      <a href={server.url} className="flex justify-between items-center bg-gray-600 p-2 rounded hover:bg-gray-500">
                        <span>{server.name}</span>
                        <span className="text-sm bg-blue-500 px-2 py-1 rounded">{server.quality}</span>
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
