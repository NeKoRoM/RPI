from litestar import Litestar, get, post

@get("/test")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}

@post("/order-count")
async def order_count(barcode: str, count: int) -> dict[str, int]:
    data = {"barcode": barcode, "count": count}
    print(data)
    return data

app = Litestar([get_book, order_count])
