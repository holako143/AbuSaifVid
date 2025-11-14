import { LatestAdditions } from './components/LatestAdditions';
import { Header } from './components/Header';
import { ContentSection } from './components/ContentSection';

function App() {
  return (
    <div className="bg-gray-900 text-white min-h-screen">
      <Header />
      <main className="container mx-auto py-8">
        <LatestAdditions />
        <ContentSection title="أحدث الأفلام" />
        <ContentSection title="أحدث المسلسلات" />
      </main>
    </div>
  );
}

export default App;
