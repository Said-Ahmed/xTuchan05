from xtuchan.products.dao import ProductDao


async def test_add_and_get_product():
    new_product = await ProductDao.add(
        name="Ролл филадельфия",
        category_id=1,
        price=450
    )

    assert new_product.category_id == 1

    new_product = await ProductDao.find_by_id(new_product.id)

    assert new_product is not None