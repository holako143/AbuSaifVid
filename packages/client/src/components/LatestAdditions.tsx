interface CardData {
  id: number;
  imageUrl: string;
  title: string;
  description: string;
  downloadLinks: { label: string; url: string }[];
}

const dummyData: CardData[] = [
  {
    id: 1,
    imageUrl: 'https://via.placeholder.com/300x200',
    title: 'فيلم جديد',
    description: 'وصف قصير للفيلم الجديد.',
    downloadLinks: [
      { label: 'تحميل مباشر - فيلم', url: '#' },
      { label: 'تورنت - فيلم', url: '#' },
    ],
  },
  {
    id: 2,
    imageUrl: 'https://via.placeholder.com/300x200',
    title: 'مسلسل جديد',
    description: 'وصف قصير للمسلسل الجديد.',
    downloadLinks: [
      { label: 'تحميل مباشر - مسلسل', url: '#' },
      { label: 'تورنت - مسلسل', url: '#' },
    ],
  },
  {
    id: 3,
    imageUrl: 'https://via.placeholder.com/300x200',
    title: 'برنامج جديد',
    description: 'وصف قصير للبرنامج الجديد.',
    downloadLinks: [
      { label: 'تحميل مباشر - برنامج', url: '#' },
      { label: 'تورنت - برنامج', url: '#' },
    ],
  },
    {
    id: 4,
    imageUrl: 'https://via.placeholder.com/300x200',
    title: 'فيلم جديد',
    description: 'وصف قصير للفيلم الجديد.',
        downloadLinks: [
      { label: 'تحميل مباشر - فيلم', url: '#' },
      { label: 'تورنت - فيلم', url: '#' },
    ],
  },
  {
    id: 5,
    imageUrl: 'https://via.placeholder.com/300x200',
    title: 'مسلسل جديد',
    description: 'وصف قصير للمسلسل الجديد.',
        downloadLinks: [
      { label: 'تحميل مباشر - مسلسل', url: '#' },
      { label: 'تورنت - مسلسل', url: '#' },
    ],
  },
  {
    id: 6,
    imageUrl: 'https://via.placeholder.com/300x200',
    title: 'برنامج جديد',
    description: 'وصف قصير للبرنامج الجديد.',
        downloadLinks: [
      { label: 'تحميل مباشر - برنامج', url: '#' },
      { label: 'تورنت - برنامج', url: '#' },
    ],
  },
];

interface LatestAdditionsProps {
  onCardClick: (downloadLinks: { label: string; url: string }[]) => void;
}

export const LatestAdditions = ({ onCardClick }: LatestAdditionsProps) => {
  const duplicatedData = [...dummyData, ...dummyData];

  return (
    <div className="relative w-full overflow-hidden">
      <h2 className="text-2xl font-bold text-center mb-8">أحدث الإضافات</h2>
      <div className="flex animate-scroll">
        {duplicatedData.map((item, index) => (
          <div
            key={`${item.id}-${index}`}
            className="flex-shrink-0 w-80 bg-gray-800 rounded-lg p-4 mx-4 cursor-pointer hover:bg-gray-700 transition-colors"
            onClick={() => onCardClick(item.downloadLinks)}
          >
            <img src={item.imageUrl} alt={item.title} className="rounded-md mb-4 object-cover h-48 w-full" />
            <div className="text-right">
              <h3 className="text-xl font-bold mb-2">{item.title}</h3>
              <p className="text-gray-400">{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
