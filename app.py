import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

# 1. Tạo dữ liệu sinh viên
data = {
    "Ho_va_ten": [
        "Huynh Le Anh Khoa", "Pham Gia Hung",
        "Le Minh Vu", "Le Gia Hoa",
        "Tran Vinh Minh Triet", "Ha Gia Huy",
        "Le Nhat Hoang Trieu", "Huynh Van Thanh",
        "Le Thi Diem", "Le Van Phuong"
    ],
    "Chuyen_can": [9, 8, 7, 10, 6, 9, 5, 8, 7, 10],
    "Giua_ky": [8, 7, 6, 9, 5, 8, 4, 7, 6, 9],
    "Cuoi_ky": [9, 8, 7, 9, 6, 9, 4, 8, 7, 10]
}

df = pd.DataFrame(data)

# 2. Tính điểm tổng kết
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# 3. Xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7:
        return "Khá"
    elif diem >= 5:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 4. Tiêu đề và bảng điểm
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

st.subheader("1. Bảng điểm 10 sinh viên")

bang_diem = df.rename(columns={
    "Ho_va_ten": "Họ và tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(bang_diem, use_container_width=True, hide_index=True)

# 5. Thống kê
st.subheader("2. Thống kê kết quả")

sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = int((df["Tong_ket"] >= 5).sum())

c1, c2 = st.columns(2)
c1.metric("Điểm trung bình lớp", f"{df['Tong_ket'].mean():.2f}")
c2.metric("Số sinh viên đạt", f"{so_sv_dat}/10")

st.write(
    f"**Điểm cao nhất:** {sv_max['Ho_va_ten']} "
    f"({sv_max['Tong_ket']:.2f})"
)
st.write(
    f"**Điểm thấp nhất:** {sv_min['Ho_va_ten']} "
    f"({sv_min['Tong_ket']:.2f})"
)

# 6. Chọn sinh viên
st.subheader("3. Tra cứu điểm sinh viên")

ten = st.selectbox("Chọn sinh viên", df["Ho_va_ten"])
sv = df[df["Ho_va_ten"] == ten].iloc[0]

st.write("**Họ và tên:**", sv["Ho_va_ten"])
st.write("**Điểm chuyên cần:**", sv["Chuyen_can"])
st.write("**Điểm giữa kỳ:**", sv["Giua_ky"])
st.write("**Điểm cuối kỳ:**", sv["Cuoi_ky"])
st.write("**Điểm tổng kết:**", f"{sv['Tong_ket']:.2f}")
st.write("**Xếp loại:**", sv["Xep_loai"])

# 7. Biểu đồ
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(df["Ho_va_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Họ và tên")
ax.set_xlim(0, 10)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# 8. Thông tin người tạo
st.divider()
st.caption("Người tạo: [Trần Trung Nghĩa] | MSSV: [056208002156]")
