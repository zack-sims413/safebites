@echo off

REM SafeBites Startup Script for Windows

echo 🚀 Starting SafeBites Application...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist "backend\.env" (
    echo 📝 Creating backend .env file...
    copy backend\env.example backend\.env
    echo ✅ Backend .env file created. Please update with your API keys.
)

REM Create frontend .env.local if it doesn't exist
if not exist "frontend\.env.local" (
    echo 📝 Creating frontend .env.local file...
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo NEXT_PUBLIC_APP_NAME=SafeBites
    ) > frontend\.env.local
    echo ✅ Frontend .env.local file created.
)

REM Start the application
echo 🐳 Starting Docker containers...
cd docker
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service status...
docker-compose ps

echo.
echo 🎉 SafeBites is starting up!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo 💡 To stop the application, run: cd docker ^&^& docker-compose down
echo 💡 To view logs, run: cd docker ^&^& docker-compose logs -f
echo.
echo ⚠️  Note: The application is running in mock mode by default.
echo    To use real API data, update backend\.env with your API keys.
echo.
pause 