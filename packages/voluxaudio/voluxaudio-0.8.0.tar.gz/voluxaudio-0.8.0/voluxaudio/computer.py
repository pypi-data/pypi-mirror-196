# site
import sounddevice as sd

def get_samplerates():
    """Return default samplerates of respective default input and output devices."""
    # NOTE: how to get default input/output id without sd.default
    # hostapis = sd.query_hostapis()
    # first_host_api = hostapis[0]
    # default_input_id = first_host_api["default_input_device"]
    # default_output_id = first_host_api["default_output_device"]

    default_input_info = sd.query_devices(sd.default.device[0])
    default_output_info = sd.query_devices(sd.default.device[1])

    # print("IN: ", default_input_info, "\nOUT: ", default_output_info, "\n")

    default_input_samplerate = int(default_input_info["default_samplerate"])
    default_output_samplerate = int(default_output_info["default_samplerate"])

    # print(
    #     "input samplerate: "
    #     + str(default_input_samplerate)
    #     + "\noutput samplerate: "
    #     + str(default_output_samplerate)
    #     + "\n"
    # )

    return (default_input_samplerate, default_output_samplerate)
