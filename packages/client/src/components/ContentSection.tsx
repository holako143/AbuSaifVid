interface ContentSectionProps {
  title: string;
}

const dummySectionData = [
  { id: 1, imageUrl: 'https://via.placeholder.com/300x450', title: 'عنوان العنصر 1' },
  { id: 2, imageUrl: 'https://via.placeholder.com/300x450', title: 'عنوان العنصر 2' },
  { id: 3, imageUrl: 'https://via.placeholder.com/300x450', title: 'عنوان العنصر 3' },
  { id: 4, imageUrl: 'https://via.placeholder.com/300x450', title: 'عنوان العنصر 4' },
  { id: 5, imageUrl: 'https://via.placeholder.com/300x450', title: 'عنوان العنصر 5' },
];

export const ContentSection = ({ title }: ContentSectionProps) => {
  return (
    <section className="my-8">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {dummySectionData.map((item) => (
          <div key={item.id} className="bg-gray-800 rounded-lg overflow-hidden transform transition-transform duration-300 hover:scale-105">
            <img src={item.imageUrl} alt={item.title} className="w-full h-96 object-cover" />
            <div className="p-4">
              <h3 className="text-lg font-bold">{item.title}</h3>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
