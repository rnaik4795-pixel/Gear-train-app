import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def gear_outline(center, radius, n_teeth, tooth_depth=0.13):
    teeth_angles = np.linspace(0, 2*np.pi, n_teeth+1)
    x, y = [], []
    for i in range(n_teeth):
        angle = teeth_angles[i]
        next_angle = teeth_angles[i+1]
        mid_angle = (angle + next_angle) / 2
        x.append(center[0] + (radius+tooth_depth)*np.cos(angle))
        y.append(center[1] + (radius+tooth_depth)*np.sin(angle))
        x.append(center[0] + (radius-tooth_depth)*np.cos(mid_angle))
        y.append(center[1] + (radius-tooth_depth)*np.sin(mid_angle))
    x.append(x[0])
    y.append(y[0])
    return np.array(x), np.array(y)

def draw_gear_train_with_teeth(diameters, labels, teeth_numbers):
    fig, ax = plt.subplots(figsize=(3*len(diameters),4))
    spacing = 1.2
    x_centers = []
    next_x = 0
    for d in diameters:
        r = d/2
        x_centers.append(next_x + r)
        next_x = x_centers[-1] + r + spacing
    ax.plot([x_centers[0]-diameters[0]/2-0.5, x_centers[-1]+diameters[-1]/2+0.5], [0,0], 'k-', lw=2)
    for i, (xc, d, lbl, n_teeth) in enumerate(zip(x_centers, diameters, labels, teeth_numbers)):
        radius = d/2
        xg, yg = gear_outline((xc,0), radius, n_teeth, tooth_depth=0.13*radius)
        ax.plot(xg, yg, color='black', lw=2)
        ax.add_patch(plt.Circle((xc,0), 0.15*radius, color='white', ec='black', lw=2))
        ax.plot([xc-0.15*radius, xc+0.15*radius], [0, 0], 'k', lw=4)
        ax.text(xc, -radius-0.5, lbl, ha='center', va='top', fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Stylized Gear Train (Calculated from Ratios)", fontsize=16)
    return fig

st.title("Gear Train Calculator with Visualization")

with st.form("gear_form"):
    module = st.number_input("Gear Module", value=2.0, step=0.1)
    base_teeth = st.number_input("Base Gear Teeth", value=20, step=1)
    input_speed = st.number_input("Input Speed (RPM)", value=1000.0, step=10.0)
    ratios_str = st.text_input("Gear Ratios (space separated)", value="2 1.5")
    submitted = st.form_submit_button("Calculate & Plot")

if submitted:
    try:
        gear_ratios = [float(x) for x in ratios_str.strip().split()]
        labels = ["Driver"]
        teeth_list = [base_teeth]
        speeds = [input_speed]
        for i, ratio in enumerate(gear_ratios):
            next_teeth = int(teeth_list[-1] * ratio)
            teeth_list.append(next_teeth)
            speeds.append(speeds[-1] / ratio)
            if i == len(gear_ratios) - 1:
                labels.append("Driven")
            elif ratio == 1:
                labels.append("Idler")
            else:
                labels.append("Driver")
        diameters = [t * module for t in teeth_list]
        st.markdown("### Gear Train Output")
        st.write(
            "| Gear | Type   | Teeth | Diameter (mm) | Speed (RPM) |\n"
            "|------|--------|-------|---------------|-------------|"
        )
        for i, (lbl, teeth, dia, speed) in enumerate(zip(labels, teeth_list, diameters, speeds), 1):
            st.write(
                f"| {i} | {lbl} | {teeth} | {dia:.2f} | {speed:.2f} |"
            )
        fig = draw_gear_train_with_teeth(diameters, labels, teeth_list)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Input error: {e}")
