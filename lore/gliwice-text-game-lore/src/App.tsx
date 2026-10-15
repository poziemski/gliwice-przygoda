import { useState, useEffect, useRef } from 'react';
import { Terminal, Map, Skull, Wifi, Database, Cpu, ChevronRight, SquareTerminal } from 'lucide-react';
import { story, StoryNode } from './gameData';

function App() {
  const [currentNodeId, setCurrentNodeId] = useState<string>('intro');
  const [history, setHistory] = useState<{ id: string, node: StoryNode, chosenText?: string }[]>([]);
  const [booting, setBooting] = useState(true);
  const [bootLines, setBootLines] = useState<string[]>([]);
  
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const fullBootSequence = [
    "> python3 run_gliwice_os.py",
    "Inicjalizacja środowiska wirtualnego...",
    "Ładowanie modułów (silesia_core.dll)... OK",
    "Sprawdzanie połączenia: Radiostacja Gliwicka... OK",
    "Wykrywanie sygnatur: Węgiel=1, Krzem=1",
    "Uruchamianie silnika narracyjnego GŁĘBIA...",
    "==============================================",
  ];

  useEffect(() => {
    let delay = 0;
    fullBootSequence.forEach((line, index) => {
      setTimeout(() => {
        setBootLines(prev => [...prev, line]);
        if (index === fullBootSequence.length - 1) {
          setTimeout(() => setBooting(false), 500);
        }
      }, delay);
      delay += 300 + Math.random() * 400; // random delay for boot effect
    });
  }, []);

  const currentNode = story[currentNodeId];

  const handleChoice = (nextId: string, choiceText: string) => {
    setHistory(prev => [...prev, { id: currentNodeId, node: currentNode, chosenText: choiceText }]);
    setCurrentNodeId(nextId);
  };

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentNodeId, history, bootLines]);

  const renderIcon = (icon?: string) => {
    switch (icon) {
      case 'terminal': return <Terminal className="w-5 h-5 text-emerald-400" />;
      case 'map': return <Map className="w-5 h-5 text-amber-400" />;
      case 'skull': return <Skull className="w-5 h-5 text-red-500" />;
      case 'wifi': return <Wifi className="w-5 h-5 text-blue-400" />;
      case 'database': return <Database className="w-5 h-5 text-purple-400" />;
      case 'cpu': return <Cpu className="w-5 h-5 text-cyan-400" />;
      default: return <ChevronRight className="w-5 h-5 text-emerald-500" />;
    }
  };

  if (booting) {
    return (
      <div className="min-h-screen bg-gray-950 text-emerald-500 p-6 font-mono selection:bg-emerald-900 selection:text-emerald-100 flex flex-col">
        <div className="max-w-3xl w-full mx-auto mt-10 space-y-2">
          {bootLines.map((line, i) => (
            <div key={i} className="animate-pulse">{line}</div>
          ))}
          <div ref={endOfMessagesRef} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-emerald-400 p-4 sm:p-6 font-mono flex flex-col overflow-x-hidden">
      <header className="max-w-3xl w-full mx-auto mb-8 border-b border-emerald-900 pb-4 flex items-center gap-3">
        <SquareTerminal className="w-8 h-8 text-emerald-500" />
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-emerald-50">PROJEKT: GLIWICE_OS</h1>
          <p className="text-xs text-emerald-700">v1.0.42 - Silesian Cyberpunk Text Adventure (Python Sim)</p>
        </div>
      </header>

      <main className="max-w-3xl w-full mx-auto flex-1 space-y-10 pb-32">
        {/* History */}
        {history.map((hist, idx) => (
          <div key={idx} className="space-y-4 opacity-60 transition-opacity hover:opacity-100">
            <div className="flex items-center gap-2 border-b border-emerald-900/50 pb-2">
              {renderIcon(hist.node.icon)}
              <h2 className="text-lg font-semibold text-emerald-200 uppercase tracking-widest">{hist.node.title}</h2>
            </div>
            <div className="space-y-3 text-emerald-600">
              {hist.node.description.map((p, i) => (
                <p key={i} className="leading-relaxed">{p}</p>
              ))}
            </div>
            {hist.chosenText && (
              <div className="mt-4 flex items-start gap-2 text-emerald-400 bg-emerald-950/30 p-3 rounded border border-emerald-900/50">
                <ChevronRight className="w-5 h-5 mt-0.5 shrink-0" />
                <p className="italic">{hist.chosenText}</p>
              </div>
            )}
          </div>
        ))}

        {/* Current Node */}
        <div className="space-y-6 animate-fade-in">
          <div className="flex items-center gap-2 border-b border-emerald-600 pb-2">
            {renderIcon(currentNode.icon)}
            <h2 className="text-xl font-bold text-emerald-50 uppercase tracking-widest">{currentNode.title}</h2>
          </div>
          <div className="space-y-4 text-emerald-300 text-lg">
            {currentNode.description.map((p, i) => (
              <p key={i} className="leading-relaxed">{p}</p>
            ))}
          </div>

          <div className="pt-6 space-y-3">
            <p className="text-sm text-emerald-600 mb-2 uppercase tracking-widest">&gt;&gt; WYBIERZ AKCJĘ:</p>
            {currentNode.choices.map((choice, i) => (
              <button
                key={i}
                onClick={() => handleChoice(choice.next, choice.text)}
                className="w-full text-left p-4 rounded bg-gray-900 border border-emerald-900 hover:border-emerald-500 hover:bg-emerald-950 transition-all flex items-start gap-3 group"
              >
                <ChevronRight className="w-5 h-5 text-emerald-700 group-hover:text-emerald-400 mt-0.5 shrink-0 transition-colors" />
                <span className="text-emerald-400 group-hover:text-emerald-100 transition-colors">{choice.text}</span>
              </button>
            ))}
          </div>
        </div>

        <div ref={endOfMessagesRef} />
      </main>

      {/* CRT Scanline overlay */}
      <div className="pointer-events-none fixed inset-0 z-50 opacity-10" style={{
        backgroundImage: 'linear-gradient(rgba(16, 185, 129, 0) 50%, rgba(16, 185, 129, 0.25) 50%)',
        backgroundSize: '100% 4px'
      }} />
    </div>
  );
}

export default App;
