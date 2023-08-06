try:
    import torch
    import tensorboard
    import torch_geometric
    import torch_sparse
except:
    raise Exception(
        "AI-based mapping algorithm need PyTorch, tensorboard, torch-geometric, and torch-sparse to run!"
    )
