function App() {
    return (
      <BrowserRouter>
        <div className={styles.app}>
        <header className={styles.appHeader}>
           <nav className={styles.appNav}>
              <Link to="/" className={styles.appLink}>Home</Link>
            </nav>
          </header>
          <main className={styles.main}>
            <Routes>
                
            </Routes>
          </main>
          <footer className={styles.footer}>
            <p>&copy; 2025 My App</p>
          </footer>
        </div>
      </BrowserRouter>
    );
  }
 
  export default App;