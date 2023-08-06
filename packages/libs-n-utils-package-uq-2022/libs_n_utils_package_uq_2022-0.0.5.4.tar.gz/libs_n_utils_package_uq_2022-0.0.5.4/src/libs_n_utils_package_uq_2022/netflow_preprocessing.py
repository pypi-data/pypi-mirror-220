from functools import lru_cache
import numpy as np
import typing as typ



# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
def generate_oh_encoder(name, categories):
    def encoder_func(x):
        v = np.zeros(len(categories), dtype='float32')
        index = np.argwhere(categories == x)[0] if isinstance(categories, np.ndarray) else categories.index(x)
        v[index] = 1.
        return v

    def decoder_func(x):
        return np.argmax(x)

    return EnhancedEncoder(name, len(categories), encoder_func, decoder_func, categorical=True, loss='categorical')






# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
def generate_clipping_encoder(name, min_value, clip_at, center_to=0., cast_func=int,
                              field_name=None, positive=True, positive_activation=False):

    field_name = name if field_name is None else field_name

    fields = f"{name}"
    sizes = [1]
    losses = 'linear' if not positive_activation else 'positive'

    def encoder_func(x):
        x -= (min_value + center_to)
        clipped = x > clip_at
        x = clip_at if clipped else x
        x *= 1. / clip_at
        return x

    def decoder_func(x):
        x = x[0]
        if np.isnan(x):
            return np.nan
        v = cast_func(x * clip_at)
        if positive and v < 0:
            v = 0
        return v

    return EnhancedEncoder(fields, sizes, encoder_func, decoder_func, loss=losses, field_names=field_name)





# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
def netflow_encoder(split_dfs):
    @lru_cache()
    def get_unique(s):
        # all = []
        # for (df_e, df_t), _ in split_dfs.values():
        #     all.append(np.unique(df_e[s].values))
        #     all.append(np.unique(df_t[s].values))
        return np.unique(split_dfs[s].values)
        # return np.unique(np.concatenate(all, axis=0))




    def encode_int8(x):
        bits = "{0:b}".format(int(x))
        bits = "0" * (8 - len(bits)) + bits
        return np.array([int(b) for b in bits], dtype="float32")

    def decode_int8(x):
        return int("".join([str(s) for s in x.astype(int)]), base=2)

    def encode_int32(x):
        bits = "{0:b}".format(int(x))
        bits = "0" * (32 - len(bits)) + bits
        return np.array([int(b) for b in bits], dtype="float32")

    def decode_int32(x):
        return int("".join([str(s) for s in x.astype(int)]), base=2)

    def encode_int16(x):
        bits = "{0:b}".format(int(x))
        bits = "0" * (16 - len(bits)) + bits
        return np.array([int(b) for b in bits], dtype="float32")

    def decode_int16(x):
        return int("".join([str(s) for s in x.astype(int)]), base=2)

    int8_enhanced_encoder = lambda s: EnhancedEncoder(s, [8], encode_int8, decode_int8, loss='categorical',
                                                      categorical=True, field_names=s)
    int16_enhanced_encoder = lambda s: EnhancedEncoder(s, [16], encode_int16, decode_int16, loss='categorical',
                                                       categorical=True, field_names=s)
    oh_enhanced_encoder = lambda s: generate_oh_encoder(s, get_unique(s))

    encoder = \
        CompositeEncoder(*([
            int8_enhanced_encoder("CLIENT_TCP_FLAGS"),
            int16_enhanced_encoder("DNS_QUERY_ID"),
            int16_enhanced_encoder("DNS_QUERY_TYPE"),
            generate_clipping_encoder("DST_TO_SRC_SECOND_BYTES", 0, 1_000_000),
            generate_clipping_encoder("DURATION_IN", 0, 2000),
            generate_clipping_encoder("DURATION_OUT", 0, 90),
            generate_clipping_encoder("FLOW_DURATION_MILLISECONDS", 0, 1236042),
            oh_enhanced_encoder("FTP_COMMAND_RET_CODE"),
            int8_enhanced_encoder("ICMP_IPV4_TYPE"),
            int16_enhanced_encoder("ICMP_TYPE"),
            generate_clipping_encoder("IN_BYTES", 0, 5000),
            generate_clipping_encoder("IN_PKTS", 0, 300),
            int16_enhanced_encoder("L4_DST_PORT"),
            int16_enhanced_encoder("L4_SRC_PORT"),
            generate_clipping_encoder("L7_PROTO", 0, 256),
            generate_clipping_encoder("LONGEST_FLOW_PKT", 0, 65535),
            generate_clipping_encoder("MAX_IP_PKT_LEN", 0, 65535),
            generate_clipping_encoder("MAX_TTL", 0, 256),
            generate_clipping_encoder("MIN_IP_PKT_LEN", 0, 700),
            generate_clipping_encoder("MIN_TTL", 0, 256),
            generate_clipping_encoder("NUM_PKTS_1024_TO_1514_BYTES", 0, 250),
            generate_clipping_encoder("NUM_PKTS_128_TO_256_BYTES", 0, 100),
            generate_clipping_encoder("NUM_PKTS_256_TO_512_BYTES", 0, 50),
            generate_clipping_encoder("NUM_PKTS_512_TO_1024_BYTES", 0, 50),
            generate_clipping_encoder("NUM_PKTS_UP_TO_128_BYTES", 0, 350),
            generate_clipping_encoder("OUT_BYTES", 0, 25_000),
            generate_clipping_encoder("OUT_PKTS", 0, 300),
            int8_enhanced_encoder("PROTOCOL"),
            generate_clipping_encoder("RETRANSMITTED_IN_BYTES", 0, 7500),
            generate_clipping_encoder("RETRANSMITTED_IN_PKTS", 0, 50),
            generate_clipping_encoder("RETRANSMITTED_OUT_BYTES", 0, 50_000),
            generate_clipping_encoder("RETRANSMITTED_OUT_PKTS", 0, 50),
            int8_enhanced_encoder("SERVER_TCP_FLAGS"),
            generate_clipping_encoder("SHORTEST_FLOW_PKT", 0, 150),
            generate_clipping_encoder("SRC_TO_DST_AVG_THROUGHPUT", 0, 29_000_000),
            generate_clipping_encoder("SRC_TO_DST_SECOND_BYTES", 0, 200_000),
            int8_enhanced_encoder("TCP_FLAGS"),
            generate_clipping_encoder("TCP_WIN_MAX_IN", 0, 65535),
            generate_clipping_encoder("TCP_WIN_MAX_OUT", 0, 65535)
        ]))
    return encoder







# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
class EnhancedEncoder:
    def __init__(self, name: typ.Union[str, typ.List[str]], shapes: typ.Union[int, typ.List[int]], encoder_func,
                 decoder_func, categorical: typ.Union[bool, typ.List[bool]] = False,
                 loss: typ.Union[str, typ.List[str]] = "mse", field_names=None):

        self.is_multi_part = (isinstance(name, list) or isinstance(name, tuple)) and (len(name) > 1)
        if field_names is None:
            assert not isinstance(name, list)

        self.field_names = name if field_names is None else field_names
        """
        The field used to generate this encoded value
        """

        if isinstance(self.field_names, str):
            self.field_names = [self.field_names]

        # we turn the name into rw_ls list always, regardless of this is truly multi-part
        if self.is_multi_part:
            self.name = list(name)
        else:
            self.name = [name]

        if self.is_multi_part:
            if isinstance(categorical, bool):
                categorical = [categorical] * len(self.name)
            else:
                assert (len(categorical) == len(self.name))

            if isinstance(loss, str):
                loss = [loss] * len(self.name)
            else:
                assert (len(loss) == len(self.name))

        # the input should be flat, regardless of the encoder output
        if isinstance(shapes, int):
            shapes = [shapes]

        self.loss = loss
        self.output_sizes = []
        self.input_size = 0
        for shape in shapes:
            self.input_size += shape
            self.output_sizes.append(shape)

        self.encoder_func = encoder_func
        self.decoder_func = decoder_func
        self.categorical = categorical

    def feed(self, *x):
        return self.encoder_func(*x)

    def decode(self, x):
        v = self.decoder_func(x)
        return [v] if not self.is_multi_part else v

    # def feed_batch(self, X):
    #     batch_size = len(X)
    #
    #     encoded = [self.encoder_func(x) for x in X]
    #
    #     feed = encoded
    #     if self.categorical:
    #         # we need to transpose this list
    #         feed = [np.array(x).reshape(batch_size, -1) for x in transpose_list_2D([flatten_simple(instance) for instance in encoded])]
    #
    #     return encoded, feed






# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
# ---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*---*
class CompositeEncoder:
    def __init__(self, *encoders: EnhancedEncoder):
        self.encoders = list(encoders)  # type: typ.List[EnhancedEncoder]
        self.evaluating_slices = []
        self.evaluating_losses = []

        self.decoding_slices = []

        # from tensorflow.keras.losses import binary_crossentropy, categorical_crossentropy, mse, mean_squared_error
        # from tensorflow.keras.layers import Dense, Concatenate

        for e in self.encoders:
        #     # print(e.name, "-->", e.loss)
        #     loss_func = binary_crossentropy if e.loss == "binary" else \
        #         categorical_crossentropy if e.loss == "categorical" \
        #             else mean_squared_error if (e.loss == "linear" or e.loss == "positive")\
        #             else None

            encoded_size = 0

            for output_size in e.output_sizes:
                cursor = 0
                if len(self.evaluating_slices) > 0:
                    cursor = self.evaluating_slices[-1][1]
                self.evaluating_slices.append((cursor, cursor + output_size))
                # self.evaluating_losses.append(loss_func)
                encoded_size += output_size

            decoding_cursor = 0
            if len(self.decoding_slices) > 0:
                decoding_cursor = self.decoding_slices[-1][1]

            self.decoding_slices.append((decoding_cursor, decoding_cursor + encoded_size))

    @property
    def input_size(self):
        return sum([e.input_size for e in self.encoders])

    @property
    def output_definition(self):
        all_definitions = []

        for e in self.encoders:
            for i in range(len(e.output_sizes)):
                all_definitions.append(
                    (e.output_sizes[i], e.loss, f"{e.name[i] if e.is_multi_part else e.name[0]}_{i + 1}"))

        return all_definitions

    def encode(self, data: dict):
        encoded = []
        for e in self.encoders:
            feed_values = [data[field_name] for field_name in e.field_names]

            # The argument approach is prefered
            # if len(feed_values) == 1:
            #     feed_values = feed_values[0]

            # print("Feed:", feed_values)

            export_data = e.feed(*feed_values)

            # print("Encoded:", export_data)

            if e.is_multi_part and isinstance(export_data, np.ndarray):
                raise Exception("If using rw_ls multipart export, the parts should be exported as rw_ls list from the encoder!")

            if e.is_multi_part:
                encoded += [np.array([e]) if not isinstance(e, np.ndarray) else e for e in export_data]
            else:
                encoded.append(np.array([export_data]) if not isinstance(export_data, np.ndarray) else export_data)

        # print("Encode yield:", encoded)
        v = np.concatenate(encoded)
        return v

    def encode_batch(self, data: typ.List[dict]):
        return np.array([self.encode(d) for d in data])

    def decode_batch(self, data: np.ndarray):
        return [self.decode(d) for d in data]

    def transform(self, x):
        return self.decode(self.encode(x))

    def transform_2D_batch(self, x):
        all = []
        for batch in x:
            instance_sequence = np.array([self.encode(b) for b in batch])
            all.append(instance_sequence)
        return all

    def transform_batch(self, x, output_reconstructed:bool=False):
        encoded = self.encode_batch(x)

        if output_reconstructed:
            return self.decode_batch(encoded), encoded

        return encoded

    def decode(self, v):
        # print("To decode:", v)
        decoded = {}
        for n, (i0, i1) in enumerate(self.decoding_slices):
            e = self.encoders[n]
            #print("DECODING ||", e, n, i0, i1, "-->", v[i0:i1])
            decoded_values = e.decode(v[i0:i1])


            for i, decoded_value in enumerate(decoded_values):
                # print("DV ||", i, decoded_value, e.name, "-->", decoded_value)
                decoded[e.name[i]] = decoded_value  # decode to the name itself

        return decoded

    def Decoder(self, x, concat=True):

        from tensorflow.keras.losses import binary_crossentropy, categorical_crossentropy, mse, mean_squared_error
        from tensorflow.keras.layers import Dense, Concatenate
        from tensorflow.keras.regularizers import l2, l1, l1_l2

        x_feed = []
        for e in self.encoders:
            for i, output_size in enumerate(e.output_sizes):
                loss_target = e.loss

                if isinstance(loss_target, list):
                    loss_target = loss_target[i]

                activation = {
                    "categorical": "softmax",
                    "linear": "linear", # linear
                    "positive": "linear", # relu
                    "binary": "sigmoid"
                }[loss_target]

                d = Dense(output_size,
                          activation=activation,
                          kernel_initializer="he_normal",
                          name=f"out_{e.name[i] if e.is_multi_part else e.name[0]}_{i + 1}_{activation}",
                          )(x) # activity_regularizer=(l1_l2() if loss_target in ["linear", "positive"] else None)


                x_feed.append(d)

        if concat:
            c = Concatenate()(x_feed)
        else:
            c = x_feed

        return c






