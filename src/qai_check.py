#https://docs.qualcomm.com/bundle/publicresource/topics/80-63442-50/introduction.html qualcomm DSK docs for implementation
#https://huggingface.co/qualcomm/Whisper-Small-En whisper



import torch
import qai_hub as hub
from qai_hub_models.models.whisper_small_en import Model

def check_qai_devices():
    devices = hub.get_devices(attributes=["chipset:qualcomm-snapdragon-x-elite"])
    print(devices)

# Load the model
model = Model.from_pretrained()
decoder_model = model.decoder
encoder_model = model.encoder

# Device
device = hub.Device("Snapdragon X Elite CRD")

# Trace model
decoder_input_shape = decoder_model.get_input_spec()
decoder_sample_inputs = decoder_model.sample_inputs()

traced_decoder_model = torch.jit.trace(decoder_model, [torch.tensor(data[0]) for _, data in decoder_sample_inputs.items()])

# Compile model on a specific device
decoder_compile_job = hub.submit_compile_job(
    model=traced_decoder_model ,
    device=device,
    input_specs=decoder_model.get_input_spec(),
)

# Get target model to run on-device
decoder_target_model = decoder_compile_job.get_target_model()
# Trace model
encoder_input_shape = encoder_model.get_input_spec()
encoder_sample_inputs = encoder_model.sample_inputs()

traced_encoder_model = torch.jit.trace(encoder_model, [torch.tensor(data[0]) for _, data in encoder_sample_inputs.items()])

# Compile model on a specific device
encoder_compile_job = hub.submit_compile_job(
    model=traced_encoder_model ,
    device=device,
    input_specs=encoder_model.get_input_spec(),
)

# Get target model to run on-device
encoder_target_model = encoder_compile_job.get_target_model()

decoder_profile_job = hub.submit_profile_job(
    model=decoder_target_model,
    device=device,
)
encoder_profile_job = hub.submit_profile_job(
    model=encoder_target_model,
    device=device,
)

decoder_input_data = decoder_model.sample_inputs()
decoder_inference_job = hub.submit_inference_job(
    model=decoder_target_model,
    device=device,
    inputs=decoder_input_data,
)
decoder_inference_job.download_output_data()
encoder_input_data = encoder_model.sample_inputs()
encoder_inference_job = hub.submit_inference_job(
    model=encoder_target_model,
    device=device,
    inputs=encoder_input_data,
)
encoder_inference_job.download_output_data()


#if __name__ == "__main__":
    #check_qai_devices()

#Snapdragon X Elite CRD
#Hexagon v73 = HTP