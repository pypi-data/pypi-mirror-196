from scNodes.core.node import *
from scNodes.core.util import apply_lut_to_float_image
import scNodes.core.settings


def create():
    return FFTNode()


class FFTNode(Node):
    title = "Fourier transform"
    group = "Custom nodes"
    colour = (178 / 255, 230 / 255, 119 / 255, 1.0)

    def __init__(self):
        super().__init__()
        self.size = 200

        self.connectable_attributes["dataset_in"] = ConnectableAttribute(ConnectableAttribute.TYPE_DATASET,
                                                                         ConnectableAttribute.INPUT, parent=self)
        self.connectable_attributes["image_out"] = ConnectableAttribute(ConnectableAttribute.TYPE_IMAGE,
                                                                        ConnectableAttribute.OUTPUT, parent=self)

    def render(self):
        if super().render_start():
            self.connectable_attributes["dataset_in"].render_start()
            self.connectable_attributes["dataset_in"].render_end()
            self.connectable_attributes["image_out"].render_start()
            self.connectable_attributes["image_out"].render_end()

            super().render_end()

    def get_image_impl(self, idx=None):
        data_source = self.connectable_attributes["dataset_in"].get_incoming_node()
        if data_source:
            frame_in = data_source.get_image(idx)
            img_in_pxd = frame_in.load()
            _w = img_in_pxd.shape[0]
            _h = img_in_pxd.shape[1]
            F = np.fft.fftshift(np.fft.fft2(img_in_pxd))
            frame_out = frame_in.clone()
            frame_out.path += " - FOURIER TRANSFORM"
            phase = apply_lut_to_float_image(np.angle(F), settings.luts["Heatmap"])
            amplitude = np.abs(F)[:, :, np.newaxis]
            frame_out.data = amplitude * phase
            return frame_out


