import numpy as np
import scipy.signal as signal
import csv

# -------------------------------
# Save/Load filter coefficients
# -------------------------------

def save_filter_to_csv(b, a, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(b)
        writer.writerow(a)
    print(f"Filter coefficients saved to {filename}")

def load_filter_from_csv(filename):
    
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        zeros = np.array(rows[0])
        poles = np.array(rows[1])
    print(f"Filter coefficients loaded from {filename}")
    return zeros, poles

# -----------------------------------
# Filter Realisation Implementations
# -----------------------------------

def filter_direct_form_ii(b, a, x):
    """
    Implements Direct Form II filtering.
    Note: a[0] is assumed nonzero; coefficients are normalized so that a[0] == 1.
    """
    b = np.array(b, dtype=float)
    a = np.array(a, dtype=float)
    if a[0] != 1:
        b = b / a[0]
        a = a / a[0]
    N = max(len(a), len(b))
    # Create delay line of length N-1 (Direct Form II uses a single delay line)
    d = np.zeros(N-1)
    y = np.zeros_like(x)
    for n in range(len(x)):
        xn = x[n]
        yn = b[0]*xn + d[0] if (N-1) > 0 else b[0]*xn
        y[n] = yn
        if N-1 > 0:
            d_new = np.zeros_like(d)
            for i in range(N-2):
                d_new[i] = b[i+1]*xn - a[i+1]*yn + d[i+1]
            d_new[-1] = b[-1]*xn - a[-1]*yn
            d = d_new
    return y

def filter_cascade(b, a, x):
    """
    Implements filter realization via cascaded second-order sections.
    Uses SciPy's tf2sos to convert the transfer function and sosfilt to filter the signal.
    """
    sos = signal.tf2sos(b, a)
    y = signal.sosfilt(sos, x)
    return y

# ---------------------------
# Export Filter to C Code
# ---------------------------

def export_filter_to_c(b, a, filename, realization='direct'):
    """
    Export filter coefficients and sample realization code to a C file.
    
    Parameters:
      - b, a: Filter coefficients.
      - filename: Name of the C file to write.
      - realization: 'direct' for Direct Form II; 'cascade' for cascaded second-order sections.
    """
    b = np.array(b, dtype=float)
    a = np.array(a, dtype=float)
    if a[0] != 1:
        b = b / a[0]
        a = a / a[0]
    b_str = ', '.join(f"{coef:.8f}" for coef in b)
    a_str = ', '.join(f"{coef:.8f}" for coef in a)
    num_b = len(b)
    num_a = len(a)
    
    if realization == 'direct':
        c_code = f"""\
/* Filter Realisation: Direct Form II */
#include <stdio.h>

#define NUM_B {num_b}
#define NUM_A {num_a}
static const double b[NUM_B] = {{ {b_str} }};
static const double a[NUM_A] = {{ {a_str} }};

/* Delay elements: NUM_A-1 */
#define N_DELAY (NUM_A - 1)
static double w[N_DELAY] = {{0}};

double filter_sample(double x) {{
    double y = b[0] * x + (N_DELAY > 0 ? w[0] : 0.0);
    for (int i = 0; i < N_DELAY - 1; i++) {{
        w[i] = b[i+1] * x - a[i+1] * y + w[i+1];
    }}
    if (N_DELAY > 0)
        w[N_DELAY-1] = b[NUM_B-1] * x - a[NUM_A-1] * y;
    return y;
}}

void reset_filter() {{
    for (int i = 0; i < N_DELAY; i++) {{
        w[i] = 0.0;
    }}
}}

int main() {{
    double input = 1.0;
    double output = filter_sample(input);
    printf("Output: %f\\n", output);
    return 0;
}}
"""
    elif realization == 'cascade':
        # Convert transfer function to second order sections
        sos = signal.tf2sos(b, a)
        num_sections = sos.shape[0]
        sections_code = ""
        for i in range(num_sections):
            section = sos[i]
            # section: [b0, b1, b2, a0, a1, a2] with a0 typically 1 after normalization.
            b0, b1, b2, a0, a1, a2 = section
            b0 /= a0; b1 /= a0; b2 /= a0; a1 /= a0; a2 /= a0;
            sections_code += f"/* Section {i+1} */\n"
            sections_code += f"static const double b_sec_{i}[3] = {{ {b0:.8f}, {b1:.8f}, {b2:.8f} }};\n"
            sections_code += f"static const double a_sec_{i}[3] = {{ 1.0, {a1:.8f}, {a2:.8f} }};\n\n"
        c_code = f"""\
/* Filter Realisation: Cascade (Second Order Sections) */
#include <stdio.h>

#define NUM_SECTIONS {num_sections}
{sections_code}
#define SECTION_ORDER 2

/* Delay states for each section */
static double w[NUM_SECTIONS][SECTION_ORDER] = {{ {{0}} }};

double filter_sample(double x) {{
    double input = x, y = 0.0;
    // For simplicity, the code below assumes only one section.
    // For multiple sections, an array of section pointers would be used.
    /* Example for section 0: */
    y = b_sec_0[0] * input + w[0][0];
    w[0][0] = b_sec_0[1] * input - a_sec_0[1] * y + w[0][1];
    w[0][1] = b_sec_0[2] * input - a_sec_0[2] * y;
    return y;
}}

void reset_filter() {{
    for (int sec = 0; sec < NUM_SECTIONS; sec++) {{
        for (int i = 0; i < SECTION_ORDER; i++) {{
            w[sec][i] = 0.0;
        }}
    }}
}}

int main() {{
    double input = 1.0;
    double output = filter_sample(input);
    printf("Output: %f\\n", output);
    return 0;
}}
"""
    else:
        raise ValueError("Unknown realisation type. Use 'direct' or 'cascade'.")
    
    with open(filename, 'w') as f:
        f.write(c_code)
    print(f"C code exported to {filename}")

# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    # Design an example Butterworth lowpass filter using SciPy.
    fs = 1000
    order = 4
    cutoff = 100
    b, a = signal.butter(order, cutoff, btype='lowpass', fs=fs)

    # Save the filter coefficients to a CSV file.
    save_filter_to_csv(b, a, "filter_coeffs.csv")

    # Load the coefficients from the CSV file.
    b_loaded, a_loaded = load_filter_from_csv("filter_coeffs.csv")

    # Create a test signal.
    t = np.linspace(0, 1, fs)
    x = np.sin(2 * np.pi * 5 * t) + 0.5 * np.random.randn(fs)

    # Apply Direct Form II filtering.
    y_direct = filter_direct_form_ii(b_loaded, a_loaded, x)
    # Apply cascade filtering.
    y_cascade = filter_cascade(b_loaded, a_loaded, x)

    # Export C code for both realizations.
    export_filter_to_c(b_loaded, a_loaded, "filter_direct.c", realization='direct')
    export_filter_to_c(b_loaded, a_loaded, "filter_cascade.c", realization='cascade')
