import React, { useState } from 'react';
import { ThemeProvider } from './contexts/ThemeContext';
import { SignIn } from './components/SignIn';
import { ChatInterface } from './components/ChatInterface';

function App() {
  const [user, setUser] = useState<string | null>(null);

  const handleSignIn = (email: string) => {
    setUser(email);
  };

  const handleSignOut = () => {
    setUser(null);
  };

  return (
    <ThemeProvider>
      <div className="min-h-screen transition-colors duration-300">
        {user ? (
          <ChatInterface userEmail={user} onSignOut={handleSignOut} />
        ) : (
          <SignIn onSignIn={handleSignIn} />
        )}
      </div>
    </ThemeProvider>
  );
}

export default App;