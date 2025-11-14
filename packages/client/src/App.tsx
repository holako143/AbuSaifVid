import { useState } from 'react';
import { Auth } from './Auth';
import { LatestAdditions } from './components/LatestAdditions';
import { DownloadModal } from './components/DownloadModal';

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedDownloadLinks, setSelectedDownloadLinks] = useState<{ label: string; url: string }[]>([]);

  const openModal = (downloadLinks: { label: string; url: string }[]) => {
    setSelectedDownloadLinks(downloadLinks);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen">
      <div className="container mx-auto py-8">
        <h1 className="text-4xl text-center mb-8">
          React 19 + Tailwind CSS 4 + tRPC
        </h1>
        <LatestAdditions onCardClick={openModal} />
        <div className="flex items-center justify-center mt-8">
          <Auth />
        </div>
        <DownloadModal
          isOpen={isModalOpen}
          onClose={closeModal}
          downloadLinks={selectedDownloadLinks}
        />
      </div>
    </div>
  );
}

export default App;
