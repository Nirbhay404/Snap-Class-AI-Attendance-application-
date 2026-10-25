from src.database.config import supabase
import bcrypt


def hash_pass(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_pass(pwd: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pwd.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# --- TEACHER DATABASE OPERATIONS ---


def check_teacher_exists(username: str) -> bool:
    username = (username or "").strip().lower()
    if not username:
        return False
    try:
        response = (
            supabase.table("teachers").select("username").eq("username", username).execute()
        )
        return len(response.data) > 0
    except Exception as e:
        print(f"Error checking teacher exists: {e}")
        return False


def create_teacher(username: str, password: str, name: str):
    username = (username or "").strip().lower()
    name = (name or "").strip()
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
    }
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username: str, password: str):
    username = (username or "").strip().lower()
    try:
        response = (
            supabase.table("teachers").select("*").eq("username", username).execute()
        )
        if response.data:
            teacher = response.data[0]
            if check_pass(password, teacher.get("password", "")):
                return teacher
    except Exception as e:
        print(f"Error in teacher_login: {e}")
    return None


def get_teacher_subjects(teacher_id):
    try:
        response = (
            supabase.table("subjects")
            .select("*")
            .eq("teacher_id", teacher_id)
            .execute()
        )
        subjects = response.data or []
        for s in subjects:
            if "total_students" not in s:
                s["total_students"] = 0
            if "total_classes" not in s:
                s["total_classes"] = 0
            if "section" not in s:
                s["section"] = "A"
        return subjects
    except Exception as e:
        print(f"Error fetching teacher subjects: {e}")
        return []


def get_attendance_for_teacher(teacher_id):
    try:
        response = (
            supabase.table("attendance")
            .select("*, subjects!inner(*)")
            .eq("subjects.teacher_id", teacher_id)
            .execute()
        )
        return response.data or []
    except Exception as e:
        print(f"Error fetching attendance records: {e}")
        return []


# --- STUDENT DATABASE OPERATIONS ---


def get_all_students():
    try:
        response = supabase.table("students").select("*").execute()
        return response.data or []
    except Exception as e:
        print(f"Error fetching students: {e}")
        return []


def create_student(name: str, face_embedding=None, voice_embedding=None):
    name = (name or "").strip()
    data = {
        "name": name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding,
    }
    try:
        response = supabase.table("students").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Error creating student: {e}")
        return None


def get_student_subjects(student_id):
    try:
        response = (
            supabase.table("subject_students")
            .select("*, subjects(*)")
            .eq("student_id", student_id)
            .execute()
        )
        return response.data or []
    except Exception as e:
        print(f"Error fetching student subjects: {e}")
        return []


def get_student_attendance(student_id):
    try:
        response = (
            supabase.table("attendance")
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )
        return response.data or []
    except Exception as e:
        print(f"Error fetching student attendance: {e}")
        return []


def unenroll_student_to_subject(student_id, subject_id):
    try:
        supabase.table("subject_students").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
        return True
    except Exception as e:
        print(f"Error unenrolling student: {e}")
        return False


def enroll_student_in_subject(student_id, subject_code: str):
    subject_code = (subject_code or "").strip().upper()
    try:
        sub_res = supabase.table("subjects").select("*").eq("subject_code", subject_code).execute()
        if not sub_res.data:
            return False, f"Subject with code '{subject_code}' not found."

        subject = sub_res.data[0]
        subject_id = subject["subject_id"]

        # Check if already enrolled
        existing = (
            supabase.table("subject_students")
            .select("*")
            .eq("student_id", student_id)
            .eq("subject_id", subject_id)
            .execute()
        )
        if existing.data:
            return False, f"Already enrolled in {subject.get('name', subject_code)}."

        supabase.table("subject_students").insert({
            "student_id": student_id,
            "subject_id": subject_id,
        }).execute()

        return True, f"Successfully enrolled in {subject.get('name', subject_code)}!"
    except Exception as e:
        return False, f"Enrollment error: {str(e)}"