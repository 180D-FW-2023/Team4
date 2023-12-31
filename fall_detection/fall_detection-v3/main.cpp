#include <stdio.h>
#include <iostream>
#include <fstream>
#include <string>
using namespace std;
#include "edge-impulse-sdk/classifier/ei_run_classifier.h"

// Callback function declaration
static int get_signal_data(size_t offset, size_t length, float *out_ptr);

// Raw features copied from test sample (Edge Impulse > Model testing)
static float input_buf[] = {
    /* Paste your raw features here! */
-3.572, -9.063,  2.341, -3.783, -9.794,  1.946, -4.017,-10.493,  2.284, -3.847, -9.727,  2.178, -3.733, -8.912,  1.927, -3.816, -8.209,  2.088, -4.359, -8.682,  2.303, -4.223, -8.656,  2.207, -4.067, -8.410,  1.839, -3.924, -8.735,  1.657, -3.936, -8.654,  1.459, -4.094, -9.290,  1.722, -4.374, -9.708,  2.353, -3.847, -8.066,  2.176, -3.867, -7.308,  2.171, -4.354, -6.872,  2.891, -4.605, -5.268,  3.455, -3.620, -3.587,  3.111, -2.231, -3.195,  1.803, -2.747, -3.950, -0.741, -1.985, -6.703, -2.535, -0.349, -2.893, -1.832, -0.163, -0.603, -1.499, -1.095, -4.161,  0.222, -3.202,-12.403,  0.562, -0.947,-12.389,  1.306, -4.240, -5.973,  0.103, -4.474, -7.867, -2.071, -6.803,-11.679,  4.409, -7.645, -9.371,  6.052, -6.205, -6.394,  4.696, -5.552, -6.110,  1.889, -5.801, -6.564,  0.096, -6.341, -6.987,  2.121, -5.715, -5.815,  0.973, -5.397, -4.407, -1.841, -5.029, -3.080, -1.318, -9.395,-12.862, -0.349, -7.910, -7.269,  1.368, -5.036, -3.168, -2.640, -0.940, -6.322, -6.707, -5.055, -6.334, -0.399, -7.461, -7.745, 15.765, -4.541, -5.194,  1.913,  0.519,-11.937, -1.186,  1.662,-22.523, -1.691, -2.764,-16.344, -1.270, -1.846, -2.126, 10.155,  5.242,  0.670,  4.321, 12.068,-32.676, -3.441, -4.299,-78.345,-42.759, -6.772, 20.005, -9.890, -7.389, 24.072,  1.884, -8.001, 19.969, 19.041,  0.729,  3.847,  8.575,  4.070,  9.297, -4.644, 12.310, -0.913, -4.302, 30.215,-66.903,-10.402,-16.832,-21.889, 78.343,  3.742,-24.020,-35.964,-34.230, 78.312,  3.343,-67.594,-21.423, 10.576, 24.063,-40.354, 28.740, 27.420, -5.858,-45.242, 10.373,  3.749,-23.981,  1.946, 18.154,-11.339,  3.336, 10.225, -5.911,  8.857, -3.231, 11.612,  8.685,-12.779, 12.028, -1.045,-14.517, 14.012,  3.556,-11.468,  6.528,  4.419,  1.506, -2.501,  5.966,  9.596, -0.741,  7.924, 10.103, -1.394, 10.053,  5.782,  0.328,  9.541,  2.083, -1.695,  7.764,  1.162,  2.202,  6.729,  0.273,  3.046,  7.415,  0.160,  3.776,  7.738, -0.036,  2.982,  7.310,  1.509,  1.179,  6.258,  5.435, -1.473,  7.013,  6.554, -4.268,  9.130,  2.166, -7.037, 11.726,  3.759, -3.393,  7.300,  6.884, -1.901,  4.955,  6.839, -5.593,  6.726, -0.777, -7.874,  9.538, -1.282, -7.200,  6.057,  8.494, -5.952,  3.494,  8.300, -0.992, 16.432, -8.221, -4.582, 13.800,-15.705,-14.536,  3.673,  1.298,  3.025, 13.266,  5.409, 11.129, 20.347, -2.114,  1.741, 11.619, -1.987, -5.760, -0.124, -0.387,-11.738,  6.966,  2.059,-17.707,  7.700,  3.986,-13.733,  3.386,  6.504, -8.639,  3.929, -0.416, -5.988,  8.857, -6.703, -2.924,  8.761, -3.747,  0.672,  5.277, -0.851, -1.090,  6.958, -1.045, -1.435,  8.362, -2.360, -2.365,  8.312, -2.709, -1.937,  8.580, -3.314, -2.970, 13.448, -6.186, -2.453,  7.198, -2.243, -4.091,  7.683, -3.355, -3.417,  7.826, -6.492, -5.820,  6.502, -7.743, -3.924,  6.573, -5.753,  0.299,  8.876, -5.806, -0.120,  5.316, -6.530, -1.700,  8.092, -9.617, -0.921,  7.671, -6.506, -0.985,  5.942, -6.437, -1.361,  6.327, -6.466, -2.135,  6.248, -8.063, -2.501,  6.081,-10.316, -1.710,  3.412, -9.699,  0.717,  3.692, -9.015,  2.513,  4.484, -7.960,  2.169,  5.165, -7.441,  1.648,  9.041, -8.788, -0.954,  5.146, -6.621, -1.289,  7.279, -6.633,  0.191,  5.258, -7.315,  1.239,  3.910, -9.393,  3.297,  2.267,-10.344,  2.977,  0.825, -9.749,  3.027,  0.648, -8.864,  2.126, -0.062, -9.189,  1.339,  0.103,-10.198,  1.798, -0.782, -9.637,  1.683, -0.772, -9.065,  1.609, -1.786, -8.336,  2.109, -1.090, -8.938,  1.499, -0.899, -8.998,  0.667,  0.433, -6.619, -1.411,  1.925, -6.860, -1.655,  0.901, -6.633, -0.648, -0.285, -7.805, -1.636, -0.866,-10.536, -1.875, -2.312,-12.389,  0.629, -3.451, -9.993,  0.693, -3.960, -9.558,  2.116, -4.065,-14.706,  3.498, -5.516,-10.352, -0.012, -5.010, -9.988,  1.064, -3.592,-10.990, -1.798, -4.888,-11.523,  3.895, -4.888,-12.339,  2.941, -3.989,-12.398,  2.473, -4.393,-11.447,  2.140, -4.943, -9.345,  2.284, -4.579, -9.440,  1.879, -5.308,-10.734,  1.846, -4.718, -9.923,  1.815, -4.390, -9.675,  0.880, -3.491, -9.096,  0.746, -3.680, -9.096,  0.650, -3.790, -9.790,  1.901, -3.484,-10.438,  2.365, -3.381,-10.328,  2.561, -2.475, -9.562,  1.985, -2.446, -8.180,  2.879, -2.551,-10.132,  2.874, -2.566,-11.734,  3.202, -2.066,-11.595,  2.975, -1.576,-10.103,  2.453,  0.112, -8.094,  1.272,  0.861, -7.886,  0.359, -0.555, -9.393,  1.490,  0.837,-11.937,  2.475,  0.756,-10.093,  1.643,  0.945, -8.338,  2.473,  1.401, -8.422,  2.597,  1.181, -9.175,  2.449,  0.980,-10.531,  2.410,  1.769, -9.330,  3.125,  3.211, -7.264,  2.544,  4.668, -6.136,  2.303,  4.940, -5.918,  0.543,  4.232, -7.757, -0.115,  3.369, -8.816,  1.810,  2.616, -8.276,  2.245,  3.505, -9.247,  1.781,  3.639,-10.576,  1.361,  3.852,-12.111,  0.923,  3.955,-11.315,  2.013,  4.880, -9.507,  2.544,  5.894,-10.010,  1.279,  6.263,-10.471,  0.581,  5.777,-10.641, -0.356,  5.509,-10.662, -0.129,  5.595, -9.914,  0.471};
float input_float_buf[600];


int main(int argc, char **argv) {

    // Reading test.txt to get the string
    fstream newfile;
    string tp;
    string complete;
    newfile.open("test.txt",ios::in);
    if(newfile.is_open()){
        while(getline(newfile, tp)){
            complete.append(tp);
        }
        newfile.close();
    }

    // cleaning up string
    complete.erase(0, 11);
    complete.pop_back();
    complete.pop_back();
    // cout << complete << "\n";

    // separating string into the numbers
    string delimiter = ",";
    size_t pos = 0;
    string token;
    string test[600];
    int count = 0;

    while ((pos = complete.find(delimiter)) != string::npos) {
        token = complete.substr(0, pos);
        test[count] = token;
        complete.erase(0, pos + delimiter.length());
        count = count + 1;
    }
    test[count] = complete;

    // cleaning up and converting numbers to float

    for(int i = 0; i < 600; i++){
        remove(test[i].begin(), test[i].end(), ' ');
        input_float_buf[i] = stof(test[i]);
        // cout << input_float_buf[i] << "\n";
    }


    signal_t signal;            // Wrapper for raw input buffer
    ei_impulse_result_t result; // Used to store inference output
    EI_IMPULSE_ERROR res;       // Return code from inference

    // Calculate the length of the buffer
    size_t buf_len = sizeof(input_float_buf) / sizeof(input_float_buf[0]);

    // Make sure that the length of the buffer matches expected input length
    if (buf_len != EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE) {
        printf("ERROR: The size of the input buffer is not correct.\r\n");
        printf("Expected %d items, but got %d\r\n",
                EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE,
                (int)buf_len);
        return 1;
    }

    // Assign callback function to fill buffer used for preprocessing/inference
    signal.total_length = EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE;
    signal.get_data = &get_signal_data;

    // Perform DSP pre-processing and inference
    res = run_classifier(&signal, &result, false);

    // Print return code and how long it took to perform inference
    printf("run_classifier returned: %d\r\n", res);
    printf("Timing: DSP %d ms, inference %d ms, anomaly %d ms\r\n",
            result.timing.dsp,
            result.timing.classification,
            result.timing.anomaly);

    // Print the prediction results (object detection)
#if EI_CLASSIFIER_OBJECT_DETECTION == 1
    printf("Object detection bounding boxes:\r\n");
    for (uint32_t i = 0; i < EI_CLASSIFIER_OBJECT_DETECTION_COUNT; i++) {
        ei_impulse_result_bounding_box_t bb = result.bounding_boxes[i];
        if (bb.value == 0) {
            continue;
        }
        printf("  %s (%f) [ x: %u, y: %u, width: %u, height: %u ]\r\n",
                bb.label,
                bb.value,
                bb.x,
                bb.y,
                bb.width,
                bb.height);
    }

    // Print the prediction results (classification)
#else
    printf("Predictions:\r\n");
    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        printf("  %s: ", ei_classifier_inferencing_categories[i]);
        printf("%.5f\r\n", result.classification[i].value);
    }
#endif

    // Print anomaly result (if it exists)
#if EI_CLASSIFIER_HAS_ANOMALY == 1
    printf("Anomaly prediction: %.3f\r\n", result.anomaly);
#endif

    return 0;
}

// Callback: fill a section of the out_ptr buffer when requested
static int get_signal_data(size_t offset, size_t length, float *out_ptr) {
    for (size_t i = 0; i < length; i++) {
        out_ptr[i] = (input_float_buf + offset)[i];
    }

    return EIDSP_OK;
}
