import { Navigate } from 'react-router-dom';

export default function TeacherProtectedRoute({ children }) {
    const isTeacherLoggedIn = localStorage.getItem('teacherLoggedIn') === 'true';
    
    if (!isTeacherLoggedIn) {
        return <Navigate to="/teacher/login" replace />;
    }
    
    return children;
}
