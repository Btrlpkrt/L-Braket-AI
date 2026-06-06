with top_left:
    st.markdown("### Seçilen tasarım")

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(0, 130)
    ax.set_ylim(0, 110)
    ax.axis("off")

    x0, y0 = 25, 20
    horizontal = min(90, 35 + l1 * 0.45)
    vertical = min(80, 25 + l2 * 0.50)

    # Parça kalınlığını veri koordinatında çiz
    bar_h = max(8, thickness * 1.2)

    # L1 yatay kol
    l1_rect = Rectangle(
        (x0, y0),
        horizontal,
        bar_h,
        facecolor="#1f77b4",
        edgecolor="none",
        zorder=1
    )
    ax.add_patch(l1_rect)

    # L2 dikey kol
    l2_rect = Rectangle(
        (x0, y0),
        bar_h,
        vertical,
        facecolor="#ff7f0e",
        edgecolor="none",
        zorder=2
    )
    ax.add_patch(l2_rect)

    # Delik L1 üzerinde
    # Teknik resim mantığı: arası beyaz, iki kenarı siyah
    hole_center_x = x0 + horizontal * 0.72

    # Çap arttıkça deliğin genişliği artsın
    hole_w = diameter * 0.32

    # Çok küçük veya aşırı büyük olmasın
    hole_w = max(4.0, min(hole_w, bar_h * 0.9))

    # Delik yüksekliği mavi parçanın içinde kalsın
    hole_h = bar_h * 0.82

    hole_left = hole_center_x - hole_w / 2
    hole_bottom = y0 + (bar_h - hole_h) / 2

    # Beyaz boşluk
    white_rect = Rectangle(
        (hole_left, hole_bottom),
        hole_w,
        hole_h,
        facecolor="white",
        edgecolor="none",
        zorder=5
    )
    ax.add_patch(white_rect)

    # Sol siyah çizgi
    ax.plot(
        [hole_left, hole_left],
        [hole_bottom, hole_bottom + hole_h],
        color="black",
        linewidth=1.8,
        zorder=6
    )

    # Sağ siyah çizgi
    ax.plot(
        [hole_left + hole_w, hole_left + hole_w],
        [hole_bottom, hole_bottom + hole_h],
        color="black",
        linewidth=1.8,
        zorder=6
    )

    # Ölçü yazıları
    ax.annotate(
        f"L1 = {l1:.0f} mm",
        xy=(x0 + horizontal / 2, y0 - 10),
        ha="center",
        fontsize=11
    )

    ax.annotate(
        f"L2 = {l2:.0f} mm",
        xy=(x0 - 10, y0 + vertical / 2),
        va="center",
        ha="center",
        rotation=90,
        fontsize=11
    )

    ax.text(
        hole_center_x,
        y0 + bar_h + 10,
        f"Ø {diameter:.1f} mm",
        va="bottom",
        ha="center",
        fontsize=10
    )

    ax.set_title(f"Et kalınlığı: {thickness:.1f} mm", fontsize=12, pad=12)

    st.pyplot(fig, use_container_width=True)
